import streamlit as st
from clef_minor.key_finder2 import finding_key
def find_key_main():
    st.title("Music Key Analyzer")

    st.write("Enter the notes separated by spaces. Use 'b' for flat and '#' for sharp.")
    #st.write()

    notes_input = st.text_input("Enter notes:", "C Eb G B")

    if st.button("Analyze"):
        if notes_input:
            results = finding_key(notes_input)
            if results:
                st.write("### Analysis Results:")
                for key, freq, scale_type in results:
                    match_percentage = freq / 7 * 100
                    st.write(f"**Key:** {key.upper()} {scale_type}")
                    st.write(f"**Match:** {match_percentage:.2f}%")
            else:
                st.write("No matching keys found.")
        else:
            st.write("Please enter some notes to analyze.")

    st.write("### How to use:")
    st.write("1. Enter the notes you want to analyze in the text box above.")
    st.write("2. Use standard notation: A, B, C, D, E, F, G")
    st.write("3. For flats, use 'b' after the note (e.g., Bb for B-flat)")
    st.write("4. For sharps, use '#' after the note (e.g., C# for C-sharp)")
    st.write("5. Separate each note with a space")
    st.write("6. Click the 'Analyze' button to see the results")
if __name__ == '__main__':
    find_key_main()
