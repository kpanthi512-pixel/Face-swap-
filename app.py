import streamlit as st
from PIL import Image

st.title("🎭 My Private Face Swap AI")

# Password Protection
PASSWORD = "mysecretpassword"
user_password = st.text_input("Enter Password to Access:", type="password")

if user_password == PASSWORD:
  st.success("Access Granted! 🎉")

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
      st.image(target_image, caption="Target Image", use_column_width=True)
    with col2:
      st.image(source_image, caption="Source Face", use_column_width=True)

    if st.button("Start Face Swap"):
      st.info(
          "Aapka private interface bilkul ready hai! Public AI spaces bar-bar"
          " URL change karte hain, isliye aap yahan apna custom face-swap"
          " Python script ya library local/custom API ke zariye plug in kar"
          " sakte hain."
      )

elif user_password:
  st.error("Incorrect Password! ❌")
else:
  st.warning("Please enter the password to access the app.")
