import streamlit as st 
from melody_key.chord_progression.notation import fun_emoji_list
from streamlit_extras.buy_me_a_coffee import button

import random
if st.button("Home"):
            support_url = "/"  # Replace with your actual support URL
            st.markdown(f'<meta http-equiv="refresh" content="0; url={support_url}">', unsafe_allow_html=True)
st.title(f"Buy me a coffee{random.choice(fun_emoji_list)}")
st.write("Making this app is not easy. Your support is appreciated. It does not have to be financially. Your feedback is also crucial. Email and Paypal email: chakhangc@yahoo.com.hk")
st.header("Payment in Hong Kong")
col1,col2=st.columns(2)
with col1:
    st.subheader("Payme")
    st.subheader("https://payme.hsbc/maxxxx1")
    
with col2:
    st.image("statics/alipay.jpeg")

st.divider()
col1,col2=st.columns(2)
with col1:
    st.subheader("Worldwide")
    button(username="maxchanhi", floating=False, width=221)
    st.write("⬆️ Click me!")
    st.subheader("Paypal email: chakhangc@yahoo.com.hk")
with col2:
    st.image("statics/paypal.jpeg")


