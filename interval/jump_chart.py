JUMP_CHART = {
    ("1","1"):"Perfect",("1","2"):"Augmented",
    ('2', '1'): "Diminished", ('2', '2'): "Minor",
    ('2', '3'): "Major", ('2', '4'): "Augmented",
    
    ('3', '3'): "Diminished",('3', '4'): "Minor",
    ('3', '5'): "Major", ('3', '6'): "Augmented",
    
    ('4', '5'): "Diminished",
    ('4', '6'): "Perfect",('4', '7'): "Augmented",
    
    ('5', '7'): "Diminished",
    ('5', '8'): "Perfect",('5', '9'): "Augmented",
    
    ('6', '8'): "Diminished",('6', '9'): "Minor",
    ('6', '10'): "Major",('6', '11'): "Augmented",
    
    ('7', '10'): "Diminished",('7', '11'): "Minor",
    ('7', '12'): "Major",('7', '13'): "Augmented",

    ('0', '10'): "Diminished",('0', '11'): "Minor",
    ('0', '12'): "Major",('0', '13'): "Augmented",
    
    ('1', '12'): "Diminished",
    ('1', '13'): "Perfect",('1', '14'): "Augmented",
}
import streamlit as st
import pandas as pd
import numpy as np

# Create the DataFrame
df = pd.DataFrame(
    {"Letter Count\\Quality": ["2nd(9th)", "3rd(10th)", "4th(11th)", "5th(12th)", "6th(13th)", "7th(14th)", "8ve(Octave)"],
     "Diminished": [1, 3, 5, 7, 8, 10, 12],
     "Minor": [2, 4, None, None, 9, 11, None],
     "Perfect": [None, None, 6, 8, None, None, 13],
     "Major": [3, 5, None, None, 10, 12, None],
     "Augmented": [4, 6, 7, 9, 11, 13, 14]}
)

int_to_order={2:"2nd(9th)",3:"3rd(10th)",4:"4th(11th)",5:"5th(12th)",6:"6th(13th)",7:"7th(14th)",8:"8ve(Octave)"}

def highlight_result(letter=int, semi=8):
    
    if letter > 1:
        letter = letter% 7
        if letter ==0:letter =7
        if letter == 1:letter =8
        
        row_index = df.index[df["Letter Count\\Quality"] == int_to_order[letter]][0]
        
        # Find the column name for the given semitone count
        col_name = None
        for col in df.columns[1:]:  # Skip the "Quality\Letter Count" column
            if df.loc[row_index, col] == semi:
                col_name = col
                break

        def style_df(data, props=''):
            row_mask = pd.Series(data.index == row_index, index=data.index)
            col_mask = pd.Series(data.columns == col_name, index=data.columns)
            return pd.DataFrame(
                np.where(
                    row_mask.values[:, np.newaxis] | col_mask.values,
                    props,
                    ''
                ),
                index=data.index,
                columns=data.columns
            )
        
        # Convert numeric columns to integers
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df_int = df.copy()
        df_int[numeric_columns] = df_int[numeric_columns].fillna(-1).astype(int).replace(-1,None)
        
        # Apply the styling and display the DataFrame
        styled_df = df_int.style.apply(style_df, props='background-color: lightyellow', axis=None)
        # Center-align all cells and set a fixed width
        styled_df = styled_df.set_properties(**{
            'text-align': 'center',
            'width': '100px',
            'height': '35px',
            'font-size': '16px'
        })
        
        def format_cell(val):
            if pd.isna(val):
                return None
            elif isinstance(val, (int, float)):
                return f'{val:.0f}'
            else:
                return str(val)

        # Apply the custom formatter
        styled_df = styled_df.format(format_cell)
        
        st.dataframe(styled_df, hide_index=True)
    else:
        st.warning("Table is not available")
        st.stop()

