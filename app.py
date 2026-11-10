import streamlit as st
from PIL import Image

st.title("🎭 My Private Face / Head Swap AI")

# Password Protection
PASSWORD = "mysecretpassword"
user_password = st.text_input("Enter Password to Access:", type="password")

if user_password == PASSWORD:
  st.success("Access Granted! 🎉")

  # Hugging Face Token check
  try:
    hf_token = st.secrets["HF_TOKEN"]
    st.info("Hugging Face Token loaded successfully!")
  except Exception:
    st.warning("⚠️ HF_TOKEN is missing in Streamlit Secrets.")
    hf_token = None

  uploaded_target = st.file_uploader(
      "Upload Target Image", type=["jpg", "png", "jpeg"]
  )
  uploaded_source = st.file_uploader(
      "Upload Source Face Image", type=["jpg", "png", "jpeg"]
  )

  if uploaded_target and uploaded_source:
    target_image = Image.open(uploaded_target)
    source_image = Image.open(uploaded_source)

    col1, col2 = st.columns(2)
    with col1:
      st.image(target_image, caption="Target Image")
    with col2:
      st.image(source_image, caption="Source Face")

    if st.button("Start Face Swap"):
      st.success("App is running successfully with your Hugging Face setup!")

elif user_password:
  st.error("Incorrect Password! ❌")
else:
  st.warning("Please enter the password to access the app.")
