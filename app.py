import streamlit as st
from research import graph

st.title("Financial Investment AI Assistant")

company_name = st.text_input("Enter the Organization Name")

if st.button("Create Report"):
    if company_name.strip():
        with st.spinner("Creating Report..."):
            result = graph.invoke({"query": company_name})

        st.subheader("Investment Facts")
        st.write(result["facts"])
        st.subheader("Investment Score")
        st.write(result["score"])

        st.subheader("Final Recommendation")
        st.write(result["final_response"])
    else:
        st.warning("Please enter a company name.")