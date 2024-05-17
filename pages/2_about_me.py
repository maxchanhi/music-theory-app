import streamlit as st

if st.button("Home"):
    support_url = "/main_app" 
    st.markdown(f'<meta http-equiv="refresh" content="0; url={support_url}">', unsafe_allow_html=True)
st.title("About me😄")
st.write("Hi there, I am Max. I began my musical journey playing the flute and pursued both my Bachelor's and Master's degrees at Hong Kong Baptist University. During my undergraduate studies, I took up the bassoon as my second instrument, flute was my major instrument, that is quite important. After graduating from HKBU, I pursued a Master of Composition degree at the Royal Birmingham Conservatoire. I also taught myself Python so I can hop on the AI hype train. I am now back in Hong Kong, developing an app while start learning the clarinet.")
st.write("Huge thanks to my composition teachers in UK: Andrew Toovey and Ed Bennett. My flute teacher: Brian Chan and Olivier Nowak. My bassoon teacher: Angel Cheung")
st.success("For more feedback, information or lessons, please contact me at: chakhangc@yahoo.com.hk. Also see my YouTube channel: https://www.youtube.com/channel/UCeJw45clCLOABqXxKhHoAlA")
st.caption("A huge credit goes to my girlfriend, Phoebe, who has been a tremendous support and has provided many fun ideas.")
