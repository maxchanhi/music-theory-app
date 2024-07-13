import streamlit as st
from interval.interval_calculator import interval_calculation,note_calculation
from interval.element import note_letters,advance_accidentals,accidentals_lilypond,reversed_accidentals_lilypond,RE_NUM_PLACEMENT
from streamlit_js_eval import streamlit_js_eval
from interval.ava_option import quality_selection_callback,all_quality
from interval.piano_keyboard.note_tranlate import create_note_list
import streamlit.components.v1 as components
from interval.jump_chart import highlight_result
def Calculate_Interval(lower_pitch_letter,lower_pitch_acc,higher_pitch_letter,higher_pitch_acc):
    lower_pitch = lower_pitch_letter.lower()+accidentals_lilypond[lower_pitch_acc]
    higher_pitch = higher_pitch_letter.lower()+accidentals_lilypond[higher_pitch_acc]
    quality, interval,letter_count = interval_calculation(lower_pitch, higher_pitch)
    if quality and interval:
        html_content,letter_show,semitone_count = create_note_list(lower_pitch,higher_pitch)
        st.success(f"The interval is a {quality} {interval}")
        st.write(f"1st count the letters: The distance is {letter_count} letters. \n{letter_show}")
        st.write("2nd count the semitones:")
        components.html(html_content,height=210)
        st.write(f"The distance is {semitone_count} semitones")
        st.write(f"Let's remember the data: {letter_count} letters and {semitone_count} semitones")
        highlight_result(letter_count,semitone_count)
        st.write(f"The interval is a {quality} {interval}")
    else:
        st.error("Invalid interval input")

def Find_Note(note, quality, interval):
    result_note,cal_semi = note_calculation(note, quality, interval)
    if result_note:
        display= result_note[0].upper()+" "+reversed_accidentals_lilypond[result_note[1:]]
        st.success(f"The resulting note is {display}")
        if interval != "Unison":
            st.write(f"Let's locate the data: {quality} and {interval}. \nIt is {cal_semi}.")
            highlight_result(int(RE_NUM_PLACEMENT[interval]),int(cal_semi))
            html_find,letter_show,count_letter=create_note_list(note, result_note)
            st.write(f"Count {cal_semi} semitones.")
            components.html(html_find,height=210)
            st.write(f"Count the letter: {letter_show}. The note must start with {letter_show[-1]}. The answer is {display}")
    else:
        st.error("Invalid input")


def in_calculator_main():
    page_width = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH',  want_output = True,)
    st.title("Music Interval and Note Calculator")

    tab1, tab2 = st.tabs(["Interval Calculation", "Note Calculation"])
    if page_width is None:
        page_width = 800 
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
                quality = st.selectbox("Select Quality", options=all_quality)
                quality_list = quality_selection_callback(quality)
            with col2:
                accidental = st.selectbox("Select Accidental", options=advance_accidentals)
                interval = st.selectbox("Select Interval", options=quality_list)
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
                quality = st.selectbox("Select Quality", options=all_quality)
                quality_list = quality_selection_callback(quality)
            with col2:
                accidental = st.selectbox("Select Accidental", options=advance_accidentals)
                interval = st.selectbox("Select Interval", options=quality_list)
            note = letter.lower()+accidentals_lilypond[accidental]
            if st.button("Find Note"):
                Find_Note(note, quality, interval)
            
if __name__ == "__main__":
    in_calculator_main()
