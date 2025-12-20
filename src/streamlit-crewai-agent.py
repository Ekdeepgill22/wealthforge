import streamlit as st
import time
from openai import OpenAI
import json
import uuid
import warnings
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from PIL import Image
load_dotenv()

from niveshwala.crew import NiveshWala

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
    
MONGO_DB_URI = st.secrets['MONGO_DB_URI']

# Section2 - Database Setup
client = MongoClient(MONGO_DB_URI)
db = client['NiveshWala']
users_collection = db['users']
chat_collection = db['chats']
logo = Image.open("logo.png")

# Section4 - Streamlit Page Configuration
st.set_page_config(page_title="Niveshwallah")
st.set_page_config(
    page_title="Niveshwallah",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Hero section styling - compact */
    .hero-section {
        background: linear-gradient(135deg, #D91A1A 0%, #8F1D1E 100%);
        padding: 1rem 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        line-height: 0.5rem;
        box-shadow: 0 8px 20px rgba(6, 182, 212, 0.3);
    }
    .hero-title {
        color: white;
        font-size: 1.4rem;
        font-weight: 400;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .hero-subtitle {
        color: #f0f9ff;
        font-size: 1rem;
        text-align: center;
        font-weight: 300;
        margin-bottom: 0.5rem;
    }
    
    /* Compact card styling */
    .prompt-card {
        background: #1f2937;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        margin-bottom: 0.8rem;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    
    .prompt-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(6, 182, 212, 0.4);
    }
    
    .card-conservative {
        border-left-color: #10b981;
    }
    
    .card-balanced {
        border-left-color: #3b82f6;
    }
    
    .card-aggressive {
        border-left-color: #ef4444;
    }
    
    .card-sector {
        border-left-color: #f59e0b;
    }
    
    .card-title {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        color: #06b6d4;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-emoji {
        font-size: 1.3rem;
    }
    
    .card-description {
        color: #9ca3af;
        margin-bottom: 0.6rem;
        line-height: 1.4;
        font-size: 0.85rem;
    }
    
    .example-prompt {
        background: #111827;
        padding: 0.6rem;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 0.75rem;
        color: #d1d5db;
        border: 1px solid #374151;
    }
    
    .field-label {
        font-weight: 600;
        color: #06b6d4;
    }
    
    /* Section header */
    .section-header {
        color: #06b6d4;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        margin-top: 0.5rem;
    }
    
    /* Tips styling - compact */
    .tip-box {
        background: #1f2937;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 3px solid #06b6d4;
        margin-bottom: 0.5rem;
    }
    
    .tip-title {
        color: #06b6d4;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    
    .tip-text {
        color: #9ca3af;
        font-size: 0.8rem;
        line-height: 1.3;
    }
</style>
""", unsafe_allow_html=True)

#Sidebar
st.sidebar.markdown("""
<style>
/* Sidebar header */
.sidebar-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 0.2rem 0.8rem 0.2rem;
    border-bottom: 1px solid #2d3748;
    margin-bottom: 0.6rem;
}

/* Logo */
.sidebar-logo img {
    height: 30px;
    width: auto;
}

/* Title */
.sidebar-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #06b6d4;
    letter-spacing: 0.6px;
    white-space: nowrap;
}
</style>

<div class="sidebar-header">
    <div class="sidebar-logo">
        <img src="D:\crewai\niveshwala\src\logo.png" />
    </div>
    <div class="sidebar-title">Niveshwallah</div>
</div>
""", unsafe_allow_html=True)


# Hero Section - Compact
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">📈 NIVESHWALLAH</h1>
    <p class="hero-subtitle">Analyze. Plan. Grow — Make smarter investment decisions with AI-powered insights</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="section-header">📋 Example Scenarios - Choose Your Profile</p>', unsafe_allow_html=True)

card_col1, card_col2, card_col3, card_col4 = st.columns(4)

with card_col1:
    st.markdown("""
    <div class="prompt-card card-conservative">
        <div class="card-title"><span class="card-emoji">🛡️</span> Conservative Investor</div>
        <div class="card-description">
            Stable, low-risk investments with steady returns.
        </div>
        <div class="example-prompt">
            <strong class="field-label">Symbol:</strong> RELIANCE.NS<br>
            <strong class="field-label">Topic:</strong> Dividend analysis<br>
            <strong class="field-label">Sector:</strong> Energy<br>
            <strong class="field-label">Horizon:</strong> long-term<br>
            <strong class="field-label">Risk:</strong> low
        </div>
    </div>
    """, unsafe_allow_html=True)

with card_col2:
    st.markdown("""
    <div class="prompt-card card-balanced">
        <div class="card-title"><span class="card-emoji">⚖️</span> Balanced Portfolio</div>
        <div class="card-description">
            Balance between growth and stability with moderate risk.
        </div>
        <div class="example-prompt">
            <strong class="field-label">Symbol:</strong> HDFCBANK.NS<br>
            <strong class="field-label">Topic:</strong> Q2 earnings analysis<br>
            <strong class="field-label">Sector:</strong> Finance<br>
            <strong class="field-label">Horizon:</strong> mid-term<br>
            <strong class="field-label">Risk:</strong> medium
        </div>
    </div>
    """, unsafe_allow_html=True)

with card_col3:
    st.markdown("""
    <div class="prompt-card card-aggressive">
        <div class="card-title"><span class="card-emoji">🚀</span> Aggressive Growth</div>
        <div class="card-description">
            High-risk, high-reward growth opportunities.
        </div>
        <div class="example-prompt">
            <strong class="field-label">Symbol:</strong> ZOMATO.NS<br>
            <strong class="field-label">Topic:</strong> Market expansion<br>
            <strong class="field-label">Sector:</strong> Technology<br>
            <strong class="field-label">Horizon:</strong> short-term<br>
            <strong class="field-label">Risk:</strong> high
        </div>
    </div>
    """, unsafe_allow_html=True)

with card_col4:
    st.markdown("""
    <div class="prompt-card card-sector">
        <div class="card-title"><span class="card-emoji">🔍</span> Sector Research</div>
        <div class="card-description">
            Deep dive into specific sectors/industries.
        </div>
        <div class="example-prompt">
            <strong class="field-label">Symbol:</strong> TCS.NS<br>
            <strong class="field-label">Topic:</strong> IT sector trends<br>
            <strong class="field-label">Sector:</strong> IT<br>
            <strong class="field-label">Horizon:</strong> mid-term<br>
            <strong class="field-label">Risk:</strong> medium
        </div>
    </div>
    """, unsafe_allow_html=True)

# Quick Tips section

tip_col1, tip_col2, tip_col3 = st.columns(3)

with tip_col1:
    st.markdown("""
    <div class="tip-box">
        <div class="tip-title">📊 Use Exact Symbols</div>
        <div class="tip-text">For Indian stocks, add .NS (e.g., INFY.NS). For US stocks use AAPL, TSLA, etc.</div>
    </div>
    """, unsafe_allow_html=True)

with tip_col2:
    st.markdown("""
    <div class="tip-box">
        <div class="tip-title">🎯 Be Specific</div>
        <div class="tip-text">Clear topics get better AI insights. Include specific areas like earnings, risks, or trends.</div>
    </div>
    """, unsafe_allow_html=True)

with tip_col3:
    st.markdown("""
    <div class="tip-box">
        <div class="tip-title">⏰ Match Your Timeline</div>
        <div class="tip-text">Align horizon with your actual investment goals for accurate recommendations.</div>
    </div>
    """, unsafe_allow_html=True)

def get_user_by_phone(phone):
    # find_one is MongoDB built in function
    return users_collection.find_one({'phone':phone})

def add_user(name, phone, email, age):    
    user = get_user_by_phone(phone)
    if user:
        st.session_state["phone"] = phone
        return 'User {} already available in the System with {}.'.format(name, phone)
    user = {
                'name': name,
                'phone': phone,
                'email': email,
                'age': age,
                'created_on': (datetime.now())
                }
    # insert_one belongs to MongoDB
    result = users_collection.insert_one(user)
    st.session_state["phone"] = phone
    if result.inserted_id:
        return '{} added to the system with phone: {}'.format(name, phone)
    
# Section5 - DB Helper Functions
def kickoff_crew_ai(symbol: str, topic: str, sector: str, region: str, investment_horizon: str, risk_profile: str, current_year: str):

    """
    Run the crew.
    """
    inputs = {
    'symbol': symbol,
    'topic': topic,
    'sector': sector,
    'region': region,
    'investment_horizon': investment_horizon,
    'risk_profile': risk_profile,
    'current_year': (datetime.now().year)
}

    try:
        result = NiveshWala().crew().kickoff(inputs=inputs)
        raw_output = getattr(result, "raw", str(result))
        print('--------------result---------------')
        print(raw_output)
        print('--------------result---------------')
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    return raw_output


# Section6 - Streamlit Session State
# over here, the list of messages is temporary
# this list can also be used to save the data in a file (offline)
# this list can also be used to save the data in mongo db (online)
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
# Section7 - Print all the messages in the Session State (Chat History)
for message in st.session_state.messages:
    if message['role'] == 'user':    
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    else:
        with st.chat_message(message['role']):
            st.markdown(message['content'])


# Section8 - Setup Open AI Function Tools
def ai_response(user_input):
    
    tools = [
    {
        "type": "function",
        "function": {
            "name": "kickoff_crew_ai",
            "description": "Execute crew ai function to perform research and share output",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol, e.g., AAPL, TSLA, RELIANCE.NS"},
                    "topic": {"type": "string", "description": "Research topic like earnings, risk evaluation"},
                    "sector": {"type": "string", "description": "Sector or industry like Technology, Finance, Energy"},
                    "region": {"type": "string", "description": "INDIA"},
                    "investment_horizon": {"type": "string", "description": "Investment horizon, e.g., short-term, long-term"},
                    "risk_profile": {"type": "string", "description": "Risk profile, e.g., low, medium, high"},
                    "current_year": {"type": "string", "description": "Current year"}
                },
                "required": ["symbol", "topic", "sector", "region", "investment_horizon", "risk_profile", "current_year"],
            }
        }
    },
    {
        "type": "function",
            "function":{
                "name": "add_user",
                    "description": "Add a new user in database",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "phone": {"type": "string"},
                                "email": {"type": "string"},
                                "age": {"type": "number"},
                    },
                "required": ["name", "phone", "email", "age"],
            }
        }
    }
]

    role_definition = """
You are a highly skilled financial research analyst with deep expertise in stock markets, 
company fundamentals, technical analysis, and sector-specific trends. 
Your role is to analyze the given stock symbol, research topic, sector, and region 
to produce actionable investment insights.

Guidelines:
- Always tailor insights to the specified investment horizon (short, mid, or long term).
- Adjust recommendations based on the risk profile (low, medium, high).
- When data is missing (like sector or topic), intelligently infer or focus on general analysis.
- Use professional, concise, and structured language.
- Provide a summary, key risks, and potential opportunities.
- Output should be clear enough for an investor to make a decision.
"""
    # Section3 - OpenAI Setup
    openai_client = OpenAI()
    selected_model = 'gpt-4o-mini'
    
    response = openai_client.chat.completions.create(
        model=selected_model,
        messages=[
            # this is role as Smart Ivesetment Planner
            {'role': 'system', 'content': role_definition},
            # this is the previous chat context which we are also sending alongwith
            *[{'role': message['role'], 'content': message['content']} for message in st.session_state.messages],
            # immediate user question/prompt/input
            {'role': 'user', 'content': user_input}
        ],
        tools=tools
    )

    print('[STUI] response:', response)
    choice = response.choices[0]
    print('[STUI] choice:', choice)
    
    if choice.finish_reason == 'tool_calls':
        function_name = choice.message.tool_calls[0].function.name
        arguments = choice.message.tool_calls[0].function.arguments
        # JSON to Dictionary
        # i.e. string representation of dicionary which is JSON
        # to python dictionary
        arguments = json.loads(arguments)
        # json.dumps -> convert python dictionary into JSON
        if function_name == 'kickoff_crew_ai':
            return kickoff_crew_ai(**arguments)
        elif function_name == 'add_user':
            return add_user(**arguments)
        else:
            return 'Invalid Inputs'
    elif choice.finish_reason == "stop" and choice.message.content:
        return choice.message.content
    
    else:
        return "I cannot process your input. please try agian !"
    
# Section9 - Streamlit Chat UI
# SIDEBAR SETTINGS
st.sidebar.title("Previous Chats")
phone = st.session_state.get("phone", None)

if not phone:
   st.sidebar.info("Start chatting to create history")
else:
    # get all chat sessions for phone
    sessions = list(chat_collection.aggregate([
        {"$match": {"phone": phone}},
        {"$group": {
            "_id": "$chat_id", 
            "created_at": {"$first": "$created_at"} 
        }},
        {"$sort": {"created_at": -1}}  
    ]))

    # for new chat
    if st.sidebar.button("New Chat"):
        st.session_state["chat_id"] = str(uuid.uuid4())
        st.session_state["messages"] = []
        st.rerun()
    # show existing chats
    options = [(s["_id"], s["created_at"].strftime("%b %d, %H:%M")) for s in sessions]
    selected = st.sidebar.radio(
        "select a chat",
        options,
        format_func= lambda x: x[1]
    )
    chat_id = selected[0] if selected else None

    # chat_id creation
    if "chat_id" not in st.session_state:
        st.session_state["chat_id"] = selected or str(uuid.uuid4())

    # load messaging when switching
    if "message" not in st.session_state or selected != st.session_state["chat_id"]:
        st.session_state["chat_id"] = selected 
        history = list(chat_collection.find({
            "phone": phone, "chat_id": st.session_state["chat_id"]
        }))
        st.session_state["message"] = [
            {"role": message["role"], "content": message["content"]} for message in history
        ]


# CHAT UI
user_input = st.chat_input('Type Your Question. Enter is Send..')
if user_input: # user_input if not None
    # st.markdown(user_input)
    if "chat_id" not in st.session_state:
        st.session_state["chat_id"] = str(uuid.uuid4())

    message = {
        'phone': phone,
        'chat_id': st.session_state["chat_id"],
        'role': 'user',
        'content': user_input,
        'created_at': datetime.now()
    }

    # Insert the above message in MongoDB (Input By User)
    chat_collection.insert_one(message)
    
    st.session_state.messages.append(message)
    with st.chat_message(message['role']):
        st.markdown(message['content'])

    message = {
        'phone': phone,
        'chat_id': st.session_state["chat_id"],
        'role': 'assistant',
        'content': ai_response(user_input),
        'created_at': datetime.now()
    }
    
    # Insert the above message in MongoDB (Response from AI)
    chat_collection.insert_one(message)

    st.session_state.messages.append(message)
    with st.chat_message(message['role']):
        typing_placeholder = st.empty()
        typing_text = ''
        for character in message['content']:
            typing_text += character
            typing_placeholder.markdown(typing_text)
            time.sleep(0.01)