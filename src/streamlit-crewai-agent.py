import streamlit as st
import time
from openai import OpenAI
import json
import uuid
import warnings
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
from niveshwala.crew import NiveshWala

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
    
# Section1 - Streamlit Page Configuration
st.set_page_config(
    page_title="WealthForge",
    layout="wide",
    initial_sidebar_state="expanded"
)    

# Section2 - Database Setup
MONGO_DB_URI = st.secrets['MONGO_DB_URI']
client = MongoClient(MONGO_DB_URI)
db = client['NiveshWala']
users_collection = db['users']
chat_collection = db['chats']

# Section 3 - Page styling
st.markdown(
    """
    <style>
    .headercontainer{
    text-align: center;          
    width: 100%;
    margin-bottom: 0.5rem;
    }
    .wealthforge-title {
        color: #6EC1E4; /* light blue */
        font-size: 4.5rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-top: -4rem; 
    }
    .hero-caption {
        font-size: 1.5rem;
        font-weight: 500;
        color: #444;
    }
    .hero-subtext {
        font-size: 1rem;
        color: #666;
        max-width: 720px;
        margin: 0 auto;
    </style>
    """,
    unsafe_allow_html=True
)
# Title
st.markdown(
    """
    <div class="headercontainer">
    <div class="wealthforge-title">WealthForge</div>
     <div class="hero-caption"> 
     AI-Powered Financial Guidance for Everyone - From Beginners to Investors
    </div>
    <div class="hero-subtext">
    Make informed investment decisions with intelligent and personalized recommendations.
    </div>
    </div>
    """    
    ,unsafe_allow_html=True
)
# cards
st.markdown(
    """
    <style>
        .cards-container {
            margin-top: -1rem;
        }

        .prompt-card {
            background: #f7f9fc;
            border-radius: 14px;
            padding: 1.1rem 1.4rem;
            height: 100%;
            cursor: pointer;
            transition: all 0.25s ease;
            border: 1px solid #e6e9ef;
        }

        .prompt-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
            border-color: #d0d7e2;
        }

        .card-title {
            font-size: 1.05rem;
            font-weight: 600;
            margin-bottom: 0.2rem;
            color: #1f2937;
        }

        .card-text {
            font-size: 0.92rem;
            color: #4b5563;
            line-height: 1.45;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='cards-container'>", unsafe_allow_html=True)

row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    st.markdown(
        """
        <div class="prompt-card">
            <div class="card-title">Where should I invest?</div>
            <div class="card-text">
                I am new to investing. I live in India and want to invest for the long term with low risk.
                Where should I start?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with row1_col2:
    st.markdown(
        """
        <div class="prompt-card">
            <div class="card-title">Analyze a stock for me</div>
            <div class="card-text">
                Analyze TCS stock for long-term investment. Include risks, growth potential,
                and the current outlook for 2026.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.markdown(
        """
        <div class="prompt-card">
            <div class="card-title">Is this investment safe?</div>
            <div class="card-text">
                I am considering investing in the technology sector in India.
                Is it safe for a medium-risk investor right now?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with row2_col2:
    st.markdown(
        """
        <div class="prompt-card">
            <div class="card-title">Help me plan my investment</div>
            <div class="card-text">
                I want to invest for the next 5-10 years with moderate risk.
                Suggest a balanced investment plan suitable for India.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)


# Section4 - DB Helper Functions
def add_user(name, phone, email, age):    
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
    
# def update_user(name, phone, email, age):
#     result = users_collection.update_one(
#         {"phone": phone},  # FILTER
#         {
#             "$set": {
#                 "name": name,
#                 "email": email,
#                 "age": age,
#                 "updated_on": datetime.now()
#             }
#         }
#     )

#     st.session_state["phone"] = phone

#     if result.matched_count == 0:
#         return "User not found."

#     if result.modified_count == 1:
#         return f"{name} updated successfully."

#     return "No changes were made."

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
    'current_year': current_year
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


# Section 5 - Streamlit Session State
# over here, the list of messages is temporary
# this list can also be used to save the data in a file (offline)
# this list can also be used to save the data in mongo db (online)
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
# Section 6 - Print all the messages in the Session State (Chat History)
for message in st.session_state.messages:
    if message['role'] == 'user':    
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    else:
        with st.chat_message(message['role']):
            st.markdown(message['content'])


# Section 7 - Setup Open AI Function Tools
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
    # {
    #     "type": "function",
    #         "function":{
    #             "name": "update_user",
    #                 "description": "Update an existing user in database",
    #                     "parameters": {
    #                         "type": "object",
    #                         "properties": {
    #                             "name": {"type": "string"},
    #                             "phone": {"type": "string"},
    #                             "email": {"type": "string"},
    #                             "age": {"type": "number"},
    #                 },
    #             "required": ["name", "phone", "email", "age"],
    #         }
    #     }
    # }
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
    
    # Section 8 - OpenAI Setup
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
    
# Section 9 - Streamlit Chat UI
phone = st.session_state.get("phone", None)
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# CHAT UI
user_input = st.chat_input("Type your question. Press Enter to send.",
    disabled=st.session_state.is_generating)

if user_input and not st.session_state.is_generating:
    st.session_state.is_generating = True
    if "chat_id" not in st.session_state:
        st.session_state["chat_id"] = str(uuid.uuid4())

    user_message = {
        'phone': phone,
        'chat_id': st.session_state["chat_id"],
        'role': 'user',
        'content': user_input,
        'created_at': datetime.now()
    }

    # Insert the above message in MongoDB (Input By User)
    chat_collection.insert_one(user_message)
    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        with st.spinner("WealthForge is thinking..."):
            ai_text = ai_response(user_input)

            typing_text = ""
            for char in ai_text:
                typing_text += char
                placeholder.markdown(typing_text)
                time.sleep(0.01)

    assistant_message = {
        'phone': phone,
        'chat_id': st.session_state["chat_id"],
        'role': 'assistant',
        'content': ai_text,
        'created_at': datetime.now()
    }
    
    # Insert the above message in MongoDB (Response from AI)
    chat_collection.insert_one(assistant_message)
    st.session_state.messages.append(assistant_message)

    st.session_state.is_generating = False