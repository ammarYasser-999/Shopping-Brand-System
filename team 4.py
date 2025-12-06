import streamlit as st
st.title("Payment Page")
if 'payment_success' not in st.session_state:
    st.session_state['payment_success'] = False

payment_method = st.radio("Choose Payment Method:", ("Visa", "Cash"))

st.write("---")

if payment_method == "Visa":
    st.subheader("Visa Details")
    visa_number = st.text_input("Enter Visa Number (16 digits)", max_chars=16)
    cvv_number = st.text_input("Enter CVV (3 digits)", max_chars=3, type="password")
    if st.button("Submit Payment") or st.session_state['payment_success']:
        errors = False
        if not st.session_state['payment_success']:
            if len(visa_number) != 16 or not visa_number.isdigit():
                st.error("Warning: Visa number must be exactly 16 digits.")
                errors = True
            if len(cvv_number) != 3 or not cvv_number.isdigit():
                st.error("Warning: CVV must be exactly 3 digits.")
                errors = True
        
        if not errors:
            st.session_state['payment_success'] = True
            st.success("Payment successful")
            st.balloons()
            st.write("---")
            st.write("### We value your feedback!")
            sentiment_mapping = ["one", "two", "three", "four", "five"]
            selected = st.feedback("stars")
            if selected is not None:
                st.markdown(f"You rated: {sentiment_mapping[selected]} star(s).")
                feedback_text = st.text_area("Please write your comment here:")
                
                if st.button("Submit Feedback"):
                    if feedback_text:
                        st.success("Thank you for your feedback!")
                    else:
                        st.warning("Please write something before submitting.")

elif payment_method == "Cash":
    st.info("You can pick up from your nearest branch.")
    st.snow()
    st.write("---")
    st.write("### We value your feedback!")
    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")
    if selected is not None:
        st.markdown(f"You rated: {sentiment_mapping[selected]} star(s).")
        feedback_text = st.text_area("Please write your comment here:")
        if st.button("Submit Feedback"):
            if feedback_text:
                st.success("Thank you for your feedback!")
            else:
                st.warning("Please write something before submitting.")