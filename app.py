import streamlit as st
from gradio_client import Client
from PIL import Image

st.title("🎭 My Private Face Swap AI")

# Password Protection
PASSWORD = "mysecretpassword"
user_password = st.text_input("Enter Password to Access:", type="password")

if user_password == PASSWORD:
  st.success("Access Granted! 🎉")

  # Hugging Face Token check from secrets
  try:
    hf_token = st.secrets["HF_TOKEN"]
  except Exception:
    hf_token = None

  uploaded_target = st.file_uploader(
      "Upload Target Image (Jisme face lagana hai)", type=["jpg", "png", "jpeg"]
  )
  uploaded_source = st.file_uploader(
      "Upload Source Face Image (Jiska face swap karna hai)",
      type=["jpg", "png", "jpeg"],
  )

  if uploaded_target and uploaded_source:
    target_path = "target.jpg"
    source_path = "source.jpg"

    with open(target_path, "wb") as f:
      f.write(uploaded_target.getbuffer())
    with open(source_path, "wb") as f:
      f.write(uploaded_source.getbuffer())

    col1, col2 = st.columns(2)
    with col1:
      st.image(uploaded_target, caption="Target Image", use_column_width=True)
    with col2:
      st.image(uploaded_source, caption="Source Face", use_column_width=True)

    if st.button("Start Face Swap"):
      with st.spinner("Processing Face Swap... Please wait (10-20 seconds)"):
        try:
          # Stable active space connection
          client = Client("omniedge/face-swap", token=hf_token)
          result = client.predict(
              input_image=target_path,
              swap_image=source_path,
              api_name="/predict",
          )

          result_image = Image.open(result)
          st.image(
              result_image, caption="Swapped Result", use_column_width=True
          )
          st.success("Face Swap Successful! 🎉")
        except Exception as e:
          st.error(
              f"Error: {e}. (Aapka token aur images theek hain, server response"
              " ka intezaar karein)"
          )

elif user_password:
  st.error("Incorrect Password! ❌")
else:
  st.warning("Please enter the password to access the app.")
  
