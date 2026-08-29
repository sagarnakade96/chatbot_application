# The below frontend code is provided by AWS and Streamlit. I have only modified it to make it look attractive.
import streamlit as st 
import rag_backend as demo ### replace rag_backend with your backend filename

st.set_page_config(page_title="HR Q and A with RAG") ### Modify Heading

new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">HR Q & A with RAG 🎯</p>'
st.markdown(new_title, unsafe_allow_html=True) ### Modify Title

@st.cache_resource(show_spinner=False)
def get_vector_index():
    index = demo.hr_index()

    if index is None:
        raise RuntimeError("Vector index creation returned None.")

    return index


with st.spinner("Creating/loading the HR policy index..."):
    try:
        vector_index = get_vector_index()
    except Exception as error:
        st.error(f"Index initialization failed: {str(error)}")
        st.stop()


input_text = st.text_area("Input text", label_visibility="collapsed") 
go_button = st.button("Mirana Web", type="primary") ### Button Name

if go_button:     
    with st.spinner("📢Anytime someone tells me that I can't do something, I want to do it more - Taylor Swift"): ### Spinner message
        response_content = demo.rag_response(
            index=vector_index,
            question=input_text,
        )
        st.write(response_content) 