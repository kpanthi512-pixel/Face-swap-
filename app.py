import streamlit as st
from PIL import Image

st.set_page_config(page_title="My Private Face Swap AI", page_layout="centered")

st.title("🎭 My Private Face / Head Swap AI")

# Yahan apna koi bhi password rakh lijiye jo aapko yaad rahe
PASSWORD = "mysecretpassword"

user_password = st.text_input("Enter Password to Access:", type="password")

if user_password == PASSWORD:
  st.success("Access Granted! 🎉")

  # Hugging Face Token check karna
  try:
    hf_token = st.secrets["HF_TOKEN"]
    st.info("Hugging Face Token successfully loaded!")
  except Exception:
    st.warning(
        "⚠️ HF_TOKEN abhi Streamlit Secrets me add nahi kiya gaya hai. (Isse"
        " hum baad me set kar lenge)"
    )
    hf_token = None

  uploaded_target = st.file_uploader(
      "Upload Target Image (Jisme face lagana hai)", type=["jpg", "png", "jpeg"]
  )
  uploaded_source = st.file_uploader(
      "Upload Source Face Image (Jiska face swap karna hai)",
      type=["jpg", "png", "jpeg"],
  )

  if uploaded_target and uploaded_source:
    target_image = Image.open(uploaded_target)
    source_image = Image.open(uploaded_source)

    col1, col2 = st.columns(2)
    with col1:
      st.image(target_image, caption="Target Image", use_column_width=True)
    with col2:
      st.image(source_image, caption="Source Face", use_column_width=True)

    if st.button("Start Face Swap"):
      with st.spinner("Processing..."):
        st.success("Files successfully uploaded! AI processing is ready.")

elif user_password:
  st.error("Incorrect Password! ❌")
else:
  st.warning("Please enter the password to access the app.")
  
