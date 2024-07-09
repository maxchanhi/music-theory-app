import streamlit as st
from interval.interval_calculator import interval_calculation,note_calculation,accidental_translation
from interval.element import NOTE_TO_SEMITONES_LILYPOND,JUMP_CHART,RE_NUM_PLACEMENT,note_letters,advance_accidentals,accidentals_lilypond
from streamlit_js_eval import streamlit_js_eval

def Calculate_Interval(lower_pitch_letter,lower_pitch_acc,higher_pitch_letter,higher_pitch_acc):
    lower_pitch = lower_pitch_letter.lower()+accidentals_lilypond[lower_pitch_acc]
    higher_pitch = higher_pitch_letter.lower()+accidentals_lilypond[higher_pitch_acc]
    quality, interval = interval_calculation(lower_pitch, higher_pitch)
    if quality and interval:
        st.success(f"The interval is a {quality} {interval}")
    else:
        st.error("Invalid interval input")
def Find_Note(note, quality, interval):
    result_note = note_calculation(note, quality, interval)
    if result_note:
        display_note = result_note
        for k, v in accidental_translation.items():
            display_note = display_note.replace(v, k)
        display_note= display_note[0].upper()+" "+display_note[1:]
        st.success(f"The resulting note is {display_note}")
    else:
        st.error("Invalid input")

page_width = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH',  want_output = True,)
def in_calculator_main(page_width):
    st.title("Music Interval and Note Calculator")

    tab1, tab2 = st.tabs(["Interval Calculation", "Note Calculation"])

    if page_width < 470:
        with tab1:
            st.header("Interval Calculation between two notes")
            col1,col2 = st.columns(2)
            with col1:
                higher_pitch_letter = st.selectbox("Select Higher Pitch", options=sorted(note_letters))
                higher_pitch_acc = st.selectbox("Select the Higher Accidental", options=advance_accidentals)
            with col2:
                lower_pitch_letter = st.selectbox("Select Lower Pitch", options=sorted(note_letters))
                lower_pitch_acc = st.selectbox("Select the Lower Accidental", options=advance_accidentals)

            if st.button("Calculate Interval"):
                Calculate_Interval(lower_pitch_letter,lower_pitch_acc,higher_pitch_letter,higher_pitch_acc)
        with tab2:
            st.header("Note Calculation from a lower note")
            col1,col2=st.columns(2)
            with col1:
                letter = st.selectbox("Select Note", options=note_letters)
                accidental = st.selectbox("Select Accidental", options=advance_accidentals)
            with col2:
                quality = st.selectbox("Select Quality", options=set(JUMP_CHART.values()))
                interval = st.selectbox("Select Interval", options=RE_NUM_PLACEMENT.keys())
            note = letter.lower()+accidentals_lilypond[accidental]
            if st.button("Find Note"):
                Find_Note(note, quality, interval)
    else:
        with tab1:
            st.header("Interval Calculation between two notes")
            col1,col2 = st.columns(2)
            with col1:
                higher_pitch_letter = st.selectbox("Select Higher Pitch", options=sorted(note_letters))
                lower_pitch_letter = st.selectbox("Select Lower Pitch", options=sorted(note_letters))
            with col2:
                higher_pitch_acc = st.selectbox("Select the Higher Accidental", options=advance_accidentals)
                lower_pitch_acc = st.selectbox("Select the Lower Accidental", options=advance_accidentals)

            if st.button("Calculate Interval"):
                Calculate_Interval(lower_pitch_letter,lower_pitch_acc,higher_pitch_letter,higher_pitch_acc)

        with tab2:
            st.header("Note Calculation from a lower note")
            col1,col2=st.columns(2)
            with col1:
                letter = st.selectbox("Select Note", options=note_letters)
                quality = st.selectbox("Select Quality", options=set(JUMP_CHART.values()))
            with col2:
                accidental = st.selectbox("Select Accidental", options=advance_accidentals)
                interval = st.selectbox("Select Interval", options=RE_NUM_PLACEMENT.keys())
            note = letter.lower()+accidentals_lilypond[accidental]
            if st.button("Find Note"):
                Find_Note(note, quality, interval)
            
if __name__ == "__main__":
    in_calculator_main(page_width)
