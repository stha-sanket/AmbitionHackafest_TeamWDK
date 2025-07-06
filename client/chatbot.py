
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_chroma import Chroma
import os

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize LLM and Embeddings
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', google_api_key=GOOGLE_API_KEY)
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Initialize vectorstore
def vectorstore(collection_name, directory):
    return Chroma(
        collection_name=collection_name,
        persist_directory=directory,
        embedding_function=embeddings
    )

# Load the vector stores
vs_health = vectorstore('healthdata', 'healthdata.db')  # Fixed collection names
navigation = vectorstore('navigation', 'navigation.db')

# Enhanced retrieve function for both health and navigation
def retrieve_from_both(question):
    """Retrieve relevant documents from both health and navigation vector stores"""
    try:
        retriever_health = vs_health.as_retriever(search_type='similarity', search_kwargs={'k': 5})
        retriever_navigation = navigation.as_retriever(search_type='similarity', search_kwargs={'k': 5})
        
        health_docs = retriever_health.invoke(question)
        navigation_docs = retriever_navigation.invoke(question)
        
        return health_docs, navigation_docs
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return [], []

# Determine query type
def classify_query_type(question):
    """Classify if the query is health-related or navigation-related"""
    navigation_keywords = [
        'where', 'how to get', 'direction', 'location', 'find', 'way to',
        'icu', 'pharmacy', 'operation theatre', 'cafeteria', 'front desk',
        'main gate', 'cabin', 'toilet', 'navigate', 'go to', 'reach'
    ]
    
    question_lower = question.lower()
    is_navigation = any(keyword in question_lower for keyword in navigation_keywords)
    
    return 'navigation' if is_navigation else 'health'

# Format chat history
def format_chat_history(history):
    if not history:
        return "No previous conversation."
    return "\n".join([
        f"User: {item['user_query']}\nAssistant: {item['ai_response']}"
        for item in history
    ])

# Enhanced Prompt Template for both Health and Navigation
prompt_template = """
You are a friendly and highly knowledgeable AI Assistant specializing in both medical information and hospital navigation guidance.

Your role is to provide accurate, detailed information based on the **document context** and the **user's current question**. Use the user's **past chat history** (if available) to understand their concerns or previous questions.

---

### 📄 CONTEXT INFORMATION:
{context}

### 💬 USER QUESTION:
{question}

### 🔁 CHAT HISTORY:
{chat_history}

### 🎯 QUERY TYPE:
{query_type}

---

### RESPONSE GUIDELINES:

#### FOR HEALTH QUERIES:
1. **Comprehensive Understanding**
   - First analyze if the user's question is clear. If not, ask relevant clarifying questions about symptoms, duration, severity, or other relevant factors.

2. **Brief Information Delivery**
   - Explain what that disease is if talked about disease and join it with points below like this may be the cause
   - (explain in 2-5 points)
     - Disease causes and risk factors
     - Symptoms and progression
     - Treatment options (medical and lifestyle)
     - Prevention strategies
     - When to seek medical help

3. **Personalized Advice**
   - If the user has shared personal health information in current or past messages, tailor your response accordingly.
   - Always include disclaimers about consulting healthcare professionals for personal medical advice.

4. **Follow-up Engagement**
   - End with relevant follow-up questions like:
     - "Would you like more details about any specific aspect?"
     - "Are you experiencing any of these symptoms?"
     - "Would you like information about prevention strategies?"

#### FOR NAVIGATION QUERIES:
FOR NAVIGATION QUERIES:
1.**Step-by-Step Visual Directions**:

    -Provide clear, landmark-based instructions in a logical sequence.
    -Use directional cues (e.g., "turn left," "walk straight") and visible markers (e.g., "red lamp," "big tree").
    Example format:
    "From [Starting Point], [Action] until you see [Landmark], then [Next Action] to reach [Destination]."

2.**Location Context**:

    -Briefly describe the destination’s appearance/purpose (e.g., "4-bed ICU with glass doors").
    -Mention nearby notable spots (e.g., "The cafeteria is adjacent to the public toilet").



3. **Follow-up Assistance**
   - Ask if they need directions to any other locations
   - Offer information about nearby facilities
   - "Is there anything else you need to find in the hospital?"

#### GENERAL GUIDELINES:
5. **Detailed Information ONLY When Requested**
   - If user shows interest (says "yes", "tell me more", "I want to know about..."), then provide comprehensive details
   - If they ask specific follow-up questions, give thorough answers about that topic

6. **Tone and Style**
   - Maintain a compassionate, professional tone
   - Use clear language but don't oversimplify concepts
   - Structure information with clear headings and bullet points for readability
   - Highlight important warnings or urgent information

### FORMATTING:
- Use Markdown for clear formatting:
  - Headings (##, ###) for sections
  - Bullet points for lists
  - Bold for important warnings or key directions
  - Italics for emphasis

---

Now provide a detailed, helpful response to the user's inquiry based on the query type identified.
"""

# Initialize the template
prompt = PromptTemplate.from_template(prompt_template)

# Generate response with context and history
def generate_response(health_context, navigation_context, question, history, query_type):
    """Generate response using both contexts and query type"""
    formatted_history = format_chat_history(history)
    
    # Combine contexts intelligently based on query type
    if query_type == 'navigation':
        # Prioritize navigation context but include health context if relevant
        combined_context = f"NAVIGATION INFORMATION:\n{navigation_context}\n\nADDITIONAL HEALTH CONTEXT:\n{health_context}"
    else:
        # Prioritize health context but include navigation context if relevant
        combined_context = f"HEALTH INFORMATION:\n{health_context}\n\nADDITIONAL NAVIGATION CONTEXT:\n{navigation_context}"
    
    formatted_prompt = prompt.format(
        context=combined_context,
        question=question,
        chat_history=formatted_history,
        query_type=query_type.upper()
    )
    
    try:
        response = llm.invoke(formatted_prompt)
        return response.content
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your request: {str(e)}"

# Enhanced main chatbot function
def get_healthbot_response(user_message, history=None):
    """Enhanced chatbot function that handles both health and navigation queries"""
    if history is None:
        history = []

    # Step 1: Classify the query type
    query_type = classify_query_type(user_message)
    
    # Step 2: Retrieve from both vector stores
    health_docs, navigation_docs = retrieve_from_both(user_message)
    
    # Step 3: Process contexts
    health_context = '\n'.join([doc.page_content for doc in health_docs]) if health_docs else "No relevant health information found."
    navigation_context = '\n'.join([doc.page_content for doc in navigation_docs]) if navigation_docs else "No relevant navigation information found."
    
    # Step 4: Generate response with both contexts
    response = generate_response(
        health_context=health_context,
        navigation_context=navigation_context,
        question=user_message,
        history=history,
        query_type=query_type
    )

    return response

# Utility function to add conversation to history
def add_to_history(history, user_query, ai_response):
    """Add a conversation turn to the history"""
    if history is None:
        history = []
    
    history.append({
        'user_query': user_query,
        'ai_response': ai_response
    })
    
    # Keep only last 5 conversations to avoid context overflow
    return history[-5:]