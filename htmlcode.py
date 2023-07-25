import os
import streamlit as st

def list_html_files(folder_path):
    html_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

def main():
    st.title("HTML Report Viewer")

    # Select the HTML folder
    folder_path = st.text_input("Enter the path of the HTML folder:")

    if folder_path and os.path.exists(folder_path):
        html_files = list_html_files(folder_path)

        if not html_files:
            st.write("No HTML files found in the selected folder.")
        else:
            # Select a report to display
            selected_file = st.selectbox("Select an HTML report:", html_files)

            # Read and display the selected report
            with open(selected_file, 'r', encoding='utf-8') as file:
                report_content = file.read()
#                st.markdown(report_content, unsafe_allow_html=True)
                st.components.v1.html(report_content, height=800)
    elif folder_path and not os.path.exists(folder_path):
        st.write("Invalid folder path. Please enter a valid path.")
    else:
        st.write("Enter the path of the HTML folder in the sidebar.")

if __name__ == "__main__":
    main()
