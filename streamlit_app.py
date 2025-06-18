# streamlit_app.py

import streamlit as st
from app.youtube_extract import YouTubeExtract
from app.mongodb_handler import MongoDBHandler

yt = YouTubeExtract()
mongo = MongoDBHandler()

st.set_page_config(page_title="YouTube Data Extractor", layout="wide")
st.title("📊 YouTube Channel Data Extractor")

channel_id = st.text_input("🔗 Enter YouTube Channel ID", value="UCJFp8uSYCjXOMnkUyb3CQ3Q")

if st.button("🚀 Extract & Upload to MongoDB"):
    if channel_id:
        with st.spinner("Extracting data from YouTube..."):
            try:
                data = yt.main(channel_id)

                st.success("✅ Data fetched successfully!")

                st.info("📦 Uploading to MongoDB...")
                mongo.insert_one("channel", data['channel'])
                mongo.insert_many("playlist", data['playlist'])
                mongo.insert_many("video", data['video'])
                mongo.insert_many("comment", data['comment'])

                st.success("🎉 Data successfully inserted into MongoDB!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please provide a valid YouTube channel ID.")

if st.button("🔍 Show Sample Data"):
    if channel_id:
        with st.spinner("Loading sample data..."):
            try:
                data = yt.main(channel_id)  # Or cache a lighter version

                st.subheader("📺 Channel Info")
                st.json(data['channel'])

                st.subheader("📂 First Playlist")
                st.json(data['playlist'][0] if data['playlist'] else {})

                st.subheader("🎬 First Video")
                st.json(data['video'][0] if data['video'] else {})

                st.subheader("💬 First Comment")
                st.json(data['comment'][0] if data['comment'] else {})
            except Exception as e:
                st.error(f"❌ Error loading samples: {e}")
