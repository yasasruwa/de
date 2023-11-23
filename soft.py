import streamlit as st
import pandas as pd
from io import BytesIO


def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data


def main():
    st.title('Data Entry Application')

    # Session state initialization
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()

    # Get column names from user
    column_input = st.text_input("Enter column names, separated by commas")
    if column_input:
        columns = column_input.split(',')
        # Create a DataFrame with specified columns if it doesn't exist
        if set(columns) != set(st.session_state.df.columns):
            st.session_state.df = pd.DataFrame(columns=columns)

        # Interface for data entry
        data = {col: st.text_input(f"Enter data for {col}") for col in columns}

        if st.button('Add to DataFrame'):
            new_data = pd.DataFrame([data])
            st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)

        st.write(st.session_state.df)

        # Download button for Excel file
        if not st.session_state.df.empty:
            val = to_excel(st.session_state.df)
            st.download_button(label='Download Excel file',
                               data=val,
                               file_name='data.xlsx',
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


if __name__ == "__main__":
    main()
