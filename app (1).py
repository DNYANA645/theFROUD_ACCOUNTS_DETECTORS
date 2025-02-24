import streamlit as st
import pandas as pd
import pickle
import os
import google.generativeai as genai

# Set up Gemini AI
GOOGLE_API_KEY = "AIzaSyCYvlGS8Hxu_aGS1cZcWIJcxlZYoUMkvTs"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to get AI response
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {e}"

# Set page config
st.set_page_config(page_title="Social Media Spam & Fake Detector", page_icon="🔥", layout="wide")

# Function to load models safely
def load_model(filename):
    if os.path.exists(filename):
        return pickle.load(open(filename, "rb"))
    else:
        st.error(f"❌ Error: {filename} not found. Please train the model first.")
        return None

# Load trained models
fb_model = load_model("facebook_model.pkl")
insta_model = load_model("instagram_model.pkl")

# Main Layout
col1, col2 = st.columns([4, 1])  # Left: Main App, Right: AI Chat

with col1:
    # Sidebar Navigation
    st.sidebar.title("Navigation 🔍")
    option = st.sidebar.radio("Choose a platform:", [
        "Home 🏠",
        "Facebook Spam Detection 📘",
        "Instagram Fake Detection 📸",
        "Statistical Structure 📊",
        "About App ℹ",
        "Why We Need This App ❓"
    ])

    if option == "Home 🏠":
        st.title("Welcome to the Social Media Spam & Fake Detector 🔥")
        st.write("Detect Facebook spam posts and Instagram fake profiles using machine learning. Choose a platform from the sidebar to start.")
        st.subheader("Fraud Accounts on Social Media 🚨")
        st.write("⚠ Fake accounts contribute to misinformation and digital fraud.")
        st.write("⚠ Many are created to spread spam, phishing links, and misleading promotions.")
        st.write("⚠ Some fake profiles engage in identity theft and financial scams.")
        st.write("⚠ Automated bots manipulate trends and public perception on social media.")
        st.write("⚠ Recognizing patterns of fraudulent behavior is crucial for online safety.")
        st.write("⚠ AI-powered detection tools play a key role in identifying and eliminating fake accounts.")

    elif option == "Facebook Spam Detection 📘":
        st.title("Facebook Spam Detection 📘")
        st.write("Enter the following details:")
        
        likes = st.number_input("Number of Likes", min_value=0)
        comments = st.number_input("Number of Comments", min_value=0)
        shares = st.number_input("Number of Shares", min_value=0)
        links = st.number_input("Number of Links in Post", min_value=0)
        reactions = st.number_input("Number of Reactions", min_value=0)
        hashtags = st.number_input("Number of Hashtags Used", min_value=0)
        mentions = st.number_input("Number of Mentions in Post", min_value=0)
        captions_length = st.number_input("Caption Length (words)", min_value=0)
        media_count = st.number_input("Number of Media Files Attached", min_value=0)
        sponsored = st.selectbox("Is it a Sponsored Post?", ["No", "Yes"])
        contains_links = st.selectbox("Does it Contain External Links?", ["No", "Yes"])
        
        if st.button("Detect Spam 🚀") and fb_model is not None:
            input_data = pd.DataFrame([[likes, comments, shares, links, reactions, hashtags, mentions, captions_length, media_count, sponsored == "Yes", contains_links == "Yes"]],
                                      columns=["likes", "comments", "shares", "links", "reactions", "hashtags", "mentions", "captions_length", "media_count", "sponsored", "contains_links"])
            prediction = fb_model.predict(input_data)
            result = "Spam" if prediction[0] == 1 else "Not Spam"
            st.write(f"🟢 Prediction: {result}")
            st.balloons()
        if result == "Spam":
            st.write("❌ Reasons for Spam Detection:")
            st.write("🔗 Contains too many external links, which is a common spam indicator.")
            st.write("📢 Excessive hashtags and mentions, often used to spread spam.")
            st.write("💰 Sponsored posts without proper engagement can indicate spam.")
            st.write("⚠ High number of reactions but low comments, suggesting artificial engagement.")
            st.write("📄 Large caption length with promotional content raises suspicion.")
            st.write("📷 Media-heavy posts with minimal interaction can be spam-related.")
        else:
            st.write("✅ Reasons for Not Being Spam:")
            st.write("👍 Balanced likes, comments, and shares indicate organic engagement.")
            st.write("📝 Well-structured caption without excessive promotional content.")
            st.write("🌎 Genuine interactions from real users, not automated behavior.")
            st.write("📷 Appropriate media usage aligning with post content.")
            st.write("🔗 Limited external links, reducing spam risk.")
            st.write("💡 Engagement levels match post type, showing real user interest.")


    elif option == "Instagram Fake Detection 📸":
        st.title("Instagram Fake Detection 📸")
        
        followers = st.number_input("Number of Followers", min_value=0)
        following = st.number_input("Number of Following", min_value=0)
        posts = st.number_input("Number of Posts", min_value=0)
        engagement_rate = st.number_input("Engagement Rate (%)", min_value=0.0, step=0.1)
        likes_avg = st.number_input("Average Likes per Post", min_value=0)
        comments_avg = st.number_input("Average Comments per Post", min_value=0)
        story_views_avg = st.number_input("Average Story Views", min_value=0)
        bio_length = st.number_input("Bio Length (characters)", min_value=0)
        username_complexity = st.number_input("Username Complexity Score", min_value=0)
        verified = st.selectbox("Is the Account Verified?", ["No", "Yes"])
        profile_pic = st.selectbox("Does it Have a Profile Picture?", ["No", "Yes"])
        
        if st.button("Detect Fake Profile 🚀") and insta_model is not None:
            input_data = pd.DataFrame([[followers, following, posts, engagement_rate, likes_avg, comments_avg, story_views_avg, bio_length, username_complexity, verified == "Yes", profile_pic == "Yes"]],
                                      columns=["followers", "following", "posts", "engagement_rate", "likes_avg", "comments_avg", "story_views_avg", "bio_length", "username_complexity", "verified", "profile_pic"])
            prediction = insta_model.predict(input_data)
            result = "Fake Profile" if prediction[0] == 1 else "Real Profile"
            st.write(f"🟢 Prediction: {result}")
            st.balloons()
        if result == "Fake Profile":
            st.write("❌ Reasons for Fake Profile Detection:")
            st.write("🤖 Low engagement rate despite high followers.")
            st.write("📊 Follows significantly more accounts than followers.")
            st.write("⚠ Suspiciously high likes but low comments.")
            st.write("🕵‍♂ Username appears randomly generated or spammy.")
            st.write("📷 No profile picture or generic image used.")
            st.write("🚨 Bio lacks personal details or contains excessive links.")
        else:
            st.write("✅ Reasons for Being a Real Profile:")
            st.write("👍 Balanced follower-to-following ratio.")
            st.write("💬 Organic engagement with meaningful comments.")
            st.write("📝 Bio contains authentic personal or professional details.")
            st.write("📢 Username appears natural and not auto-generated.")
            st.write("📷 Profile picture is present and unique.")
            st.write("🔍 Engagement patterns align with real user activity.")


    elif option == "About App ℹ":
        st.title("About This App ℹ")
        st.write("🚀 This AI-powered application helps detect spam posts on Facebook and fake profiles on Instagram.")
        st.write("🤖 It utilizes machine learning models trained on real-world datasets to provide accurate results.")
        st.write("📊 Users can enter various attributes of a post or profile to determine its authenticity.")
        st.write("🔍 The app provides explanations and recommendations based on detection results.")
        st.write("💡 Helps individuals and businesses maintain a safe and trustworthy online presence.")
        st.write("🛡 Enhances social media security by identifying fraudulent activities proactively.")
        st.write("📢 Supports ethical social media engagement by reducing misinformation and scams.")
        st.write("✅ Easy to use and accessible to all users with just a few clicks!")

    elif option == "Why We Need This App ❓":
        st.title("Why We Need This App ❓")
        st.write("1️⃣ Social media platforms are filled with spam and fake accounts, misleading users.")
        st.write("2️⃣ Fake accounts are often used for scams, misinformation, and malicious activities.")
        st.write("3️⃣ AI-driven detection helps prevent fraud and enhances user safety online.")
        st.write("4️⃣ Businesses rely on authentic engagement, and filtering out fake profiles improves their reach.")
        st.write("5️⃣ Individuals can avoid interactions with fake accounts and misleading content.")
        st.write("6️⃣ Automated spam detection reduces manual moderation efforts and improves efficiency.")
        st.write("7️⃣ Helps social media platforms maintain a healthier and more genuine user base.")

    elif option == "Statistical Structure 📊":
        st.title("Statistical Analysis of Social Media Spam & Fake Accounts 📊")
        st.write("📊 Understanding the patterns behind spam and fake accounts is essential for securing online platforms. Here are some key insights:")
        st.write("1️⃣ *Spam accounts often have an unusually high number of links and hashtags*, which helps them spread misinformation quickly.")
        st.write("2️⃣ *Fake profiles tend to follow many accounts but have very few followers*, indicating artificial engagement.")
        st.write("3️⃣ *Accounts with low engagement rates are often flagged as fake*, as real users interact more consistently.")
        st.write("4️⃣ *Sponsored posts with excessive external links are more likely to be spam*, as scammers use them for phishing.")
        st.write("5️⃣ *AI models can identify these patterns to protect users*, making social media safer and more trustworthy. 🔍")

with col2:
    # AI Chat Sidebar (Collapsible)
    with st.expander("🤖 Gemini AI Chat"):
        st.write("Ask anything to Gemini AI:")
        user_query = st.text_area("Type your question here:")

        if st.button("Get AI Response 🚀"):
            with st.spinner("Thinking..."):
                ai_response = get_gemini_response(user_query)
                st.write("**Gemini AI:**", ai_response)
