
# FinBotX - AI Banking Assistant 🤖💳

**FinBotX** is an intelligent AI-powered banking assistant built using LangChain, Azure OpenAI, and various banking tools to help users manage their financial tasks. It integrates several functionalities including money transfers, address updates, and credit card payments through natural language processing (NLP). 

### Features:
- **Money Transfer:** Sends money to specified recipients.
- **Address Update:** Updates the user’s registered address.
- **Credit Card Payment:** Processes credit card bill payments.
- **Intent Detection:** Detects user intentions such as greeting or banking-related queries.
- **Conversation Memory:** Stores user interactions to offer personalized responses.
- **Easy-to-use Interface:** Built with Streamlit for a smooth, responsive user experience.

### Technologies:
- **LangChain:** For managing tools, agents, and conversation logic.
- **Azure OpenAI:** For NLP and AI-driven responses.
- **Streamlit:** For creating an interactive UI.
- **Regular Expressions (Regex):** For extracting numerical values from text inputs.

### How It Works:
1. Users interact with the assistant via a simple chat interface.
2. The AI determines the user's intent (e.g., money transfer, address update).
3. The appropriate tool is invoked, and the task is processed.
4. The assistant provides confirmation or further assistance as needed.

### Run it:
To run this project locally:
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set up the `OPENAI_API_KEY` and Azure API credentials.
4. Run the app using Streamlit: `streamlit run app.py`.
