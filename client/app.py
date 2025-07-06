# /home/ashuranoryoshi/Desktop/hsm/client/app.py
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import os
import sqlite3
from dotenv import load_dotenv
from chatbot import get_healthbot_response
import json
from PIL import Image
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session

# Configure template folder
app.template_folder = 'templates'

# Load environment variables
load_dotenv()

# Configure Google AI for digital card functionality
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    print(f"Warning: Google AI not configured: {e}")
    model = None

# Always use the absolute path to the database
DATABASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3'))
print("Flask is using database at:", DATABASE)

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    """Query the database and return results"""
    conn = get_db_connection()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def get_user_profile(user_id):
    """Get user profile from database"""
    # Use the admin user ID (1) since we don't have proper authentication
    query = "SELECT * FROM user_profiles WHERE user_id = 1"
    return query_db(query, (), one=True)

def save_user_profile(user_id, profile_data):
    """Save or update user profile in database"""
    conn = get_db_connection()
    now = datetime.now().isoformat()  # Get current timestamp

    try:
        # Check if profile exists for admin user
        existing = get_user_profile(user_id)
        
        if existing:
            # Update existing profile
            query = """
            UPDATE user_profiles 
            SET name = ?, age = ?, sex = ?, address = ?, blood_group = ?, 
                phone = ?, diagnosis = ?, clinical_summary = ?, updated_at = ?
            WHERE user_id = 1
            """
            conn.execute(query, (
                profile_data.get('name', ''),
                profile_data.get('age', ''),
                profile_data.get('sex', ''),
                profile_data.get('address', ''),
                profile_data.get('blood', ''),
                profile_data.get('phone', ''),
                profile_data.get('diagnosis', ''),
                profile_data.get('summary', ''),
                now  # Set updated_at
            ))
            print(f"Updated profile for admin user")
        else:
            # Insert new profile for admin user
            query = """
            INSERT INTO user_profiles 
            (name, age, sex, address, blood_group, phone, diagnosis, clinical_summary, created_at, updated_at, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """
            conn.execute(query, (
                profile_data.get('name', ''),
                profile_data.get('age', ''),
                profile_data.get('sex', ''),
                profile_data.get('address', ''),
                profile_data.get('blood', ''),
                profile_data.get('phone', ''),
                profile_data.get('diagnosis', ''),
                profile_data.get('summary', ''),
                now,  # Set created_at
                now   # Set updated_at
            ))
            print(f"Created new profile for admin user")

        conn.commit()
        print(f"Profile data saved successfully")

    except Exception as e:
        print(f"Error saving profile to database: {str(e)}")
        conn.rollback()
        raise e
    finally:
        conn.close()

# In-memory storage for chat history (replace with database in production)
chat_history = {}

@app.route('/')
def index():
    """Render the landing page"""
    return render_template('index.html')

@app.route('/login')
def login():
    """Render the login/signup page"""
    print(session)
    return render_template('hms.html')

@app.route('/patient-homepage')
def patient_homepage():
    """Render the patient homepage"""
    print(session)
    print("Patient homepage route accessed")  # Debug log
    # Check if user is logged in (you can add more sophisticated auth here)
    return render_template('patient_homepage.html')

@app.route('/icu')
def icu():
    """Render the ICU dashboard"""
    print("ICU route accessed")  # Debug log
    return render_template('icu.html')

@app.route('/chat')
def chat_interface():
    """Render the chat interface"""
    # Initialize session if not exists
    if 'user_id' not in session:
        session['user_id'] = os.urandom(16).hex()
        chat_history[session['user_id']] = []
    
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and return bot response"""
    if 'user_id' not in session:
        return jsonify({"error": "Session not initialized"}), 400

    user_message = request.form.get('user_message', '').strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        # Get user's chat history
        user_history = chat_history.get(session['user_id'], [])

        # Get bot response (in Markdown format)
        bot_response_markdown = get_healthbot_response(user_message, user_history)

        # Store the interaction
        timestamp = datetime.now().isoformat()
        interaction = {
            "timestamp": timestamp,
            "user_query": user_message,
            "ai_response": bot_response_markdown
        }

        user_history.append(interaction)
        chat_history[session['user_id']] = user_history

        # Return the markdown response - frontend will handle conversion
        return jsonify({"response": bot_response_markdown})

    except Exception as e:
        print(f"Error processing chat: {str(e)}")
        if "quota" in str(e).lower() or "429" in str(e):
            return jsonify({
                "error": "We're experiencing high demand. Please wait a moment and try again."
            }), 429
        return jsonify({
            "error": "Sorry, we're having trouble processing your request. Please try again later."
        }), 500

@app.route('/api/get_chat_history')
def get_chat_history():
    """Return the user's chat history"""
    if 'user_id' not in session:
        return jsonify([])
    
    return jsonify(chat_history.get(session['user_id'], []))

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """Clear the user's chat history"""
    if 'user_id' not in session:
        return jsonify({"error": "Session not initialized"}), 400
    
    chat_history[session['user_id']] = []
    return jsonify({"status": "success"})

@app.route('/api/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    # Clear session data
    session.clear()
    return jsonify({"status": "success", "message": "Logged out successfully"})

@app.route('/api/icu-data')
def get_icu_data():
    """Get ICU bed data from database"""
    try:
        # Query ICU beds from database
        query = """
        SELECT 
            bed_number,
            bed_type,
            is_occupied,
            assigned_patient,
            CASE 
                WHEN is_occupied = 1 THEN 'Occupied'
                ELSE 'Available'
            END as status
        FROM beds_bed 
        WHERE bed_type = 'ICU'
        ORDER BY bed_number
        """

        beds = query_db(query) or []

        # Convert to list of dictionaries
        icu_data = []
        for bed in beds:
            icu_data.append({
                'bed_number': bed['bed_number'],
                'bed_type': bed['bed_type'],
                'is_occupied': bool(bed['is_occupied']),
                'assigned_patient': bed['assigned_patient'] or 'No patient assigned',
                'status': bed['status'],
                'room_number': f"Room {bed['bed_number'].replace('ICU-', '')}01",
                'condition': 'Stable' if bed['is_occupied'] else '-',
                'last_updated': 'Just now'
            })

        # Calculate statistics
        total_beds = len(icu_data)
        occupied_beds = sum(1 for bed in icu_data if bed['is_occupied'])
        available_beds = total_beds - occupied_beds

        print(f"ICU Data: {icu_data}")  # Debug log
        print(f"Statistics: Total={total_beds}, Occupied={occupied_beds}, Available={available_beds}")  # Debug log

        return jsonify({
            'success': True,
            'data': icu_data,
            'statistics': {
                'total': total_beds,
                'occupied': occupied_beds,
                'available': available_beds
            }
        })
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({
            'success': False,
            'error': 'Database error: Failed to fetch ICU data'
        }), 500
    except Exception as e:
        print(f"Error fetching ICU data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch ICU data'
        }), 500

@app.route('/api/patient-data')
def get_patient_data():
    """Get patient data for the logged-in user"""
    try:
        # For now, return mock data - you can extend this to fetch from database
        # based on the logged-in user's information
        return jsonify({
            'success': True,
            'data': {
                'name': 'John Doe',
                'patient_id': 'P001',
                'current_bed': 'ICU-1',
                'condition': 'Stable',
                'admission_date': '2025-01-15'
            }
        })
    except Exception as e:
        print(f"Error fetching patient data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch patient data'
        }), 500

@app.route('/faqs')
def faqs():
    """FAQ page"""
    return render_template('faqs.html')

@app.route('/bedding')
def bedding():
    """Render the bedding page"""
    return render_template('bedding.html')

@app.route('/profile')
def profile():
    """Render the profile page"""
    return render_template('profile.html')

@app.route('/api/extract-report', methods=['POST'])
def extract_report():
    """Extract medical data from uploaded report image"""
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image uploaded"}), 400
    
    if not model:
        return jsonify({"success": False, "error": "Google AI not configured"}), 500
    
    try:
        img = Image.open(request.files['image'].stream)
        img.load()

        prompt = '''Extract medical details from this discharge summary and return STRICTLY as JSON:
        {
          "name": "Patient Name",
          "age": "Age",
          "phone": "Phone",
          "address": "Address",
          "blood_group": "Blood Type",
          "admission_date": "Admission Date",
          "discharge_date": "Discharge Date",
          "stay_duration": "Hospital Stay Duration",
          "diagnosis": ["Diagnosis 1", "Diagnosis 2"],
          "medications": [
            {
              "name": "Medicine Name",
              "dosage": "Dosage",
              "frequency": "Frequency",
              "purpose": "Purpose"
            }
          ],
          "clinical_summary": "Clinical summary text"
        }'''

        response = model.generate_content([prompt, img])
        response_text = response.text.strip()

        # Clean up JSON response
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()

        data = json.loads(response_text)
        
        # Store extracted data in session
        session['extracted_data'] = data
        
        return jsonify({
            "success": True,
            "data": data,
            "message": "Data extracted successfully"
        })

    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/bedding-data')
def get_bedding_data():
    """Get non-ICU bed data from database"""
    try:
        # Query non-ICU beds from database
        query = """
        SELECT 
            bed_number,
            bed_type,
            is_occupied,
            assigned_patient,
            CASE 
                WHEN is_occupied = 1 THEN 'Occupied'
                ELSE 'Available'
            END as status
        FROM beds_bed 
        WHERE bed_type != 'ICU'
        ORDER BY bed_number
        """
        beds = query_db(query) or []

        bedding_data = []
        for bed in beds:
            bedding_data.append({
                'bed_number': bed['bed_number'],
                'bed_type': bed['bed_type'],
                'is_occupied': bool(bed['is_occupied']),
                'assigned_patient': bed['assigned_patient'] or '-',
                'status': bed['status']
            })

        # Calculate statistics
        total_beds = len(bedding_data)
        occupied_beds = sum(1 for bed in bedding_data if bed['is_occupied'])
        available_beds = total_beds - occupied_beds

        return jsonify({
            'success': True,
            'data': bedding_data,
            'statistics': {
                'total': total_beds,
                'occupied': occupied_beds,
                'available': available_beds
            }
        })
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({
            'success': False,
            'error': 'Database error: Failed to fetch bedding data'
        }), 500
    except Exception as e:
        print(f"Error fetching bedding data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch bedding data'
        }), 500

@app.route('/api/update-profile', methods=['POST'])
def update_profile():
    """Update user profile data"""
    print(session)
    try:
        data = request.get_json()
        print(f"Received profile update request: {data}")
        
        # Get user ID from session or create one
        if 'user_id' not in session:
            session['user_id'] = os.urandom(16).hex()
        
        user_id = session['user_id']
        print(f"Processing profile update for user: {user_id}")
        
        # Save to database
        save_user_profile(user_id, data)
        
        print(f"Profile update completed successfully for user: {user_id}")
        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        })
        
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/get-profile')
def get_profile():
    """Get user profile data from database"""
    print(session)
    try:
        # Get user ID from session
        if 'user_id' not in session:
            session['user_id'] = os.urandom(16).hex()
        
        user_id = session['user_id']
        
        # Get profile from database
        profile_data = get_user_profile(user_id)
        
        if profile_data:
            # Convert SQLite Row to dictionary
            profile_dict = dict(profile_data)
            data = {
                'name': profile_dict.get('name', ''),
                'age': profile_dict.get('age', ''),
                'sex': profile_dict.get('sex', ''),
                'address': profile_dict.get('address', ''),
                'blood': profile_dict.get('blood_group', ''),
                'phone': profile_dict.get('phone', ''),
                'diagnosis': profile_dict.get('diagnosis', ''),
                'summary': profile_dict.get('clinical_summary', '')
            }
        else:
            # Return empty profile if none exists
            data = {
                'name': '',
                'age': '',
                'sex': '',
                'address': '',
                'blood': '',
                'phone': '',
                'diagnosis': '',
                'summary': ''
            }
        
        return jsonify({
            "success": True,
            "data": data
        })
        
    except Exception as e:
        print(f"Error getting profile: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/add-to-waiting-list', methods=['POST'])
def add_to_waiting_list():
    """Add user to waiting list"""
    try:
        # Get user ID from session
        if 'user_id' not in session:
            session['user_id'] = os.urandom(16).hex()
        
        user_id = session['user_id']
        
        # Get user profile from database
        profile_data = get_user_profile(user_id)
        
        if not profile_data:
            return jsonify({
                "success": False,
                "error": "User profile not found. Please complete your profile first."
            }), 400
        
        # Convert SQLite Row to dictionary
        profile_dict = dict(profile_data)
        
        conn = get_db_connection()
        
        # First, check if patient already exists
        existing_patient = conn.execute(
            "SELECT id FROM patients_patient WHERE name = ? AND phone = ?",
            (profile_dict.get('name', ''), profile_dict.get('phone', ''))
        ).fetchone()
        
        patient_id = None
        
        if existing_patient:
            patient_id = existing_patient[0]
        else:
            # Create a patient record if it doesn't exist
            patient_query = """
            INSERT INTO patients_patient 
            (name, age, sex, address, phone, guardian_name, guardian_phone, medical_history, diagnosis_report, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            now = datetime.now().isoformat()
            conn.execute(patient_query, (
                profile_dict.get('name', ''),
                profile_dict.get('age', 0),
                profile_dict.get('sex', 'O'),
                profile_dict.get('address', ''),
                profile_dict.get('phone', ''),
                profile_dict.get('name', ''),  # Using name as guardian name
                profile_dict.get('phone', ''),  # Using phone as guardian phone
                profile_dict.get('summary', ''),  # Using clinical summary as medical history
                profile_dict.get('diagnosis', ''),  # Using diagnosis as diagnosis report
                now
            ))
            
            # Get the newly created patient ID
            patient_id = conn.execute(
                "SELECT id FROM patients_patient WHERE name = ? AND phone = ?",
                (profile_dict.get('name', ''), profile_dict.get('phone', ''))
            ).fetchone()[0]
        
        # Check if user is already in waiting list
        existing_waiting = conn.execute(
            "SELECT * FROM beds_bedwaitinglist WHERE patient_id = ?", 
            (patient_id,)
        ).fetchone()
        
        if existing_waiting:
            conn.close()
            return jsonify({
                "success": False,
                "error": "You are already in the waiting list."
            }), 400
        
        # Insert into waiting list
        waiting_query = """
        INSERT INTO beds_bedwaitinglist 
        (patient_id, bed_type, requested_at)
        VALUES (?, ?, ?)
        """
        
        now = datetime.now().isoformat()
        conn.execute(waiting_query, (
            patient_id,
            'Normal',  # Default to Normal bed type
            now
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Successfully added to waiting list!"
        })
            
    except Exception as e:
        print(f"Error adding to waiting list: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5003)