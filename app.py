import io
import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image

st.title("🎭 My Private Face Swap AI")

# Password Protection
PASSWORD = "mysecretpassword"
user_password = st.text_input("Enter Password to Access:", type="password")

if user_password == PASSWORD:
  st.success("Access Granted! 🎉")

  # Hugging Face Token check
  try:
    hf_token = st.secrets["HF_TOKEN"]
    st.success("Hugging Face Token loaded successfully!")
  except Exception:
    st.error("⚠️ HF_TOKEN is missing in Streamlit Secrets.")
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
      if hf_token:
        with st.spinner("Processing Face Swap securely..."):
          try:
            # Official Hugging Face Client use kar rahe hain
            client = InferenceClient(token=hf_token)

            # Model ko client ke zariye call karna
            image_bytes = client.image_to_image(
                image=target_image,
                prompt=(
                    "face swap target with source face"
                ),  # Model prompt requirement
                model="tinside/inswapper",
            )

            st.image(
                image_bytes, caption="Swapped Result", use_column_width=True
            )
            st.success("Face Swap Successful! 🎉")
          except Exception as e:
            st.info(
                "Note: Kuch Hugging Face models free tier par load hone me thoda"
                f" waqt lete hain ya restricted hote hain. Details: {e}"
            )
      else:
        st.error("Hugging Face Token is missing!")

elif user_password:
  st.error("Incorrect Password! ❌")
else:
  st.warning("Please enter the password to access the app.")
  
