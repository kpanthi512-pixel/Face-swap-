import io
import requests
import streamlit as st
from PIL import Image

st.title("🎭 My Private Face & Video Swap AI")

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

  # Choose Mode
  option = st.selectbox(
      "Choose Swap Type", ["Photo Face Swap", "Video Face Swap"]
  )

  if option == "Photo Face Swap":
    uploaded_target = st.file_uploader(
        "Upload Target Image (Jisme face lagana hai)",
        type=["jpg", "png", "jpeg"],
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

      if st.button("Start Photo Face Swap"):
        if hf_token:
          with st.spinner(
              "Processing Face Swap via Hugging Face API..."
          ):
            # Hugging Face ka popular face swap model endpoint
            API_URL = "https://api-inference.huggingface.co/models/tinside/inswapper"
            headers = {"Authorization": f"Bearer {hf_token}"}

            # Images ko bytes me convert karna
            target_bytes = uploaded_target.getvalue()
            source_bytes = uploaded_source.getvalue()

            # API Request bhej rahe hain
            response = requests.post(
                API_URL,
                headers=headers,
                files={"target_image": target_bytes, "source_image": source_bytes},
            )

            if response.status_code == 200:
              result_image = Image.open(io.BytesIO(response.content))
              st.image(
                  result_image,
                  caption="Swapped Result",
                  use_column_width=True,
              )
              st.success("Face Swap Successful! 🎉")
            else:
              st.error(
                  f"Error from API: {response.text}. (Make sure your HF Token"
                  " has permissions)"
              )
        else:
          st.error("Hugging Face Token is missing!")

  elif option == "Video Face Swap":
    uploaded_video = st.file_uploader(
        "Upload Target Video", type=["mp4", "mov", "avi"]
    )
    uploaded_source_video = st.file_uploader(
        "Upload Source Face Image for Video", type=["jpg", "png", "jpeg"]
    )

    if uploaded_video and uploaded_source_video:
      st.video(uploaded_video)
      if st.button("Start Video Face Swap"):
        st.info(
            "Video face swap ke liye heavy GPU processing ki zaroorat hoti hai,"
            " jo cloud API par queues me chalti hai. Aap upar diye gaye photo"
            " swap ko turant use kar sakte hain!"
        )

elif user_password:
  st.error("Incorrect Password! ❌")
else:
    st.warning("Please enter the password to access the app.")
