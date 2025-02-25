import streamlit as st
from ai_engine import process_message



# ✅ Sayfa Ayarları
st.set_page_config(page_title="FinBotX - Banka Asistanı 🤖💳", page_icon="💰", layout="wide")

st.title("🤖 FinBotX - Banka Asistanı")


# **🎨 Stil ve UI Düzenleme**
st.markdown(
    """
    <style>
    .message-box {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 82%;    
    }
    .bot-message {
        background-color: #DFFFD6;
        text-align: left;
    }
    .user-message {
        background-color: #E3F2FD;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Sohbet Geçmişi Yönetimi
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Geçmiş Sohbetleri Yönetme
def reset_chat():
    if st.session_state.messages:
        st.session_state.chat_sessions.append(st.session_state.messages.copy())
    st.session_state.messages = []

# ✅ Sol Panel (Geçmiş Sohbetler)
with st.sidebar:
    st.title("📜 Geçmiş Sohbetler")
    if st.button("🆕 Yeni Sohbet Aç"):
        reset_chat()
    for idx, chat in enumerate(st.session_state.chat_sessions):
        if st.button(f"📂 Sohbet {idx+1}"):
            st.session_state.messages = chat.copy()

# ✅ Sohbet Alanı
chat_placeholder = st.empty()
with chat_placeholder.container():
    for message in st.session_state.messages:
        role, text = message["role"], message["content"]
        message_class = "bot-message" if role == "bot" else "user-message"
        st.markdown(f'<div class="message-box {message_class}">{text}</div>', unsafe_allow_html=True)

# ✅ Kullanıcı Mesajını Al ve Gönder
with st.container():
    col1, col2 = st.columns([5, 1])
    
    with col1:
        # Kullanıcı mesajını al, ancak 'key' parametresi ile önceki değeri temizlemeyin.
        user_input = st.text_input("", key="user_input", placeholder="💬 Mesajınızı buraya yazın...", label_visibility="collapsed")
    
    with col2:
        if st.button("📨", key="send_button"):
            if user_input:
                # Kullanıcı mesajını ekle
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Bot yanıtını al
                bot_response = process_message(user_input)
                
                # Bot yanıtını ekle
                st.session_state.messages.append({"role": "bot", "content": bot_response})
                
                # Sohbeti yeniden güncelle
                chat_placeholder.empty()
                with chat_placeholder.container():
                    for message in st.session_state.messages:
                        role, text = message["role"], message["content"]
                        message_class = "bot-message" if role == "bot" else "user-message"
                        st.markdown(f'<div class="message-box {message_class}">{text}</div>', unsafe_allow_html=True)
                
                # 'user_input' widget'ını sıfırlamak için yeniden render etme
                st.rerun()  # Sayfayı yeniden çalıştırarak input kutusunu sıfırlama
