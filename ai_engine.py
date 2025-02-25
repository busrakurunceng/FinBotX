import os
import time
import re
from langchain_openai import AzureChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage


os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# ✅ Azure OpenAI Bağlantısı
llm = AzureChatOpenAI(
    azure_endpoint="azure_endpoint",
    azure_deployment="azure_deployment",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_version="2024-08-01-preview",
)

# ✅ Sayı Ayıklama Fonksiyonu
def extract_amount(text: str) -> float:
    """
    Extracts the numerical amount from a text input.
    Example:
    - "5670 USD"  →  5670.0
    - "4500 TL"   →  4500.0
    - "$1234"     →  1234.0
    """
    match = re.search(r"\d+(\.\d+)?", text)
    return float(match.group()) if match else None

# ✅ Banka İşlemleri (LangChain Tools)
@tool
def money_transfer(recipient: str, amount: str) -> str:
    """Transfers a specific amount of money to a given recipient."""
    amount = extract_amount(amount)  # Sayıyı temizle
    if amount is None:
        return "⚠️ Please provide a valid amount for the transfer."
    print(f"Processing money transfer to {recipient} for {amount} TL...")
    time.sleep(2)
    return f"✅ The money transfer of {amount} TL to {recipient} has been completed successfully."

@tool
def address_update(new_address: str) -> str:
    """Updates the user's registered address."""
    print(f"Updating address to: {new_address}...")
    time.sleep(2)
    return f"✅ Your address has been updated to {new_address}."

@tool
def credit_card_payment(amount: str) -> str:
    """
    Processes a credit card bill payment.
    
    Parameters:
    - amount (str): The amount to be paid. Example: '3450 USD'
    
    Returns:
    - Confirmation message after processing the payment.
    """
    import re
    match = re.search(r"\d+(\.\d+)?", amount)
    if match:
        amount_value = float(match.group())
    else:
        return "❌ Invalid amount format. Please enter a valid number."
    
    print(f"Processing credit card payment of {amount_value} ...")
    time.sleep(2)
    return f"✅ A payment of {amount_value} has been made to your credit card."


# ✅ Hafıza (Memory) Ayarları
memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True
)

# ✅ Agent Yapısı
tools = [money_transfer, address_update, credit_card_payment]

agent = initialize_agent(
    tools=[money_transfer, address_update, credit_card_payment],  # Tool'unu burada belirtiyoruz.
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,  # Araç kullanmayı zorunlu kılar.
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

# ✅ Kullanıcı Niyet Belirleme (Intent Detection)
def detect_intent(user_input: str) -> str:
    """
    Determines the user's intent based on the given input.
    Possible intents:
    - "money_transfer"
    - "address_update"
    - "credit_card_payment"
    - "greeting"
    - "unknown" (if the intent is not recognized)
    """
    intent_prompt = f"""
    You are FinBotX, an AI banking assistant. 
    Analyze the following customer message and determine their intent.

    Possible intents:
    - "money_transfer" (if the user wants to send money to someone)
    - "address_update" (if the user wants to update their address)
    - "credit_card_payment" (if the user wants to pay a credit card bill)
    - "greeting" (if the user is just saying hello)
    - "unknown" (if their request does not match any of the above)

    Previous conversation history:
    {memory.load_memory_variables({})["chat_history"]}

    Customer message: {user_input}
    Intent:
    """
    response = llm.invoke([SystemMessage(content=intent_prompt)])
    return response.content.strip().lower()

# ✅ Mesajı İşle ve Yanıt Döndür
def process_message(user_input: str) -> str:
    """Processes the user message, detects intent, and provides an appropriate response."""
    intent = detect_intent(user_input)

    if intent == "greeting":
        return "👋 Hello! How can I assist you with your banking needs today?"
    
    elif intent == "unknown":
        return (
            "❌ I’m sorry, but I can only assist with banking-related topics such as money transfers, "
            "address updates, and credit card payments. Please let me know if you need help with any of these! 😊"
        )

    try:
        response = agent.invoke({"input": user_input})
        return response["output"]
    except Exception as e:
        return f"⚠️ An error occurred while processing your request: {str(e)}"
