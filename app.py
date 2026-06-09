import streamlit as st
import pickle
import re
import nltk
import os

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# ==========================
# LOAD MODEL FILES
# ==========================



MODEL_PATH = "models"

with open(os.path.join(MODEL_PATH, "spamora_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(MODEL_PATH, "vectorizer.pkl"), "rb") as f:
    tfidf = pickle.load(f)

with open(os.path.join(MODEL_PATH, "label_encoder.pkl"), "rb") as f:
    encoder = pickle.load(f)

# ==========================
# NLTK SETUP
# ==========================

nltk.download("stopwords")

ps = PorterStemmer()
STOPWORDS = set(stopwords.words("english"))

# ==========================
# TEXT PREPROCESSING
# ==========================

def transform_text(text):

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    words = text.split()

    cleaned = []

    for word in words:

        if word not in STOPWORDS:
            cleaned.append(
                ps.stem(word)
            )

    return " ".join(cleaned)

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Spamora AI",
    page_icon="🛡️",
    layout="centered"
)

# ==========================
# PROFESSIONAL CSS
# ==========================
st.markdown("""
<style>

/* Hide Streamlit Elements */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* ==========================
   CYBER BACKGROUND
========================== */

.stApp::after{
content:"";
position:fixed;
top:0;
left:0;
width:100%;
height:100%;

background:

radial-gradient(
circle at 20% 20%,
rgba(0,212,255,.10),
transparent 25%
),

radial-gradient(
circle at 80% 25%,
rgba(139,92,246,.08),
transparent 25%
),

radial-gradient(
circle at 50% 80%,
rgba(34,211,238,.06),
transparent 30%
);

animation:ambientGlow 10s ease-in-out infinite;

pointer-events:none;
}

/* Animated Cyber Grid */

.stApp::before{
content:"";
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background-image:
linear-gradient(rgba(0,212,255,.06) 1px, transparent 1px),
linear-gradient(90deg, rgba(0,212,255,.06) 1px, transparent 1px);
background-size:50px 50px;
animation:gridMove 15s linear infinite;
pointer-events:none;
z-index:0;
}

/* Background Glow */

.stApp::after{
content:"";
position:fixed;
top:0;
left:0;
width:100%;
height:100%;

/* Multiple Glow Sources */

background:

radial-gradient(
circle at 20% 20%,
rgba(0,212,255,.18),
transparent 25%
),

radial-gradient(
circle at 80% 25%,
rgba(139,92,246,.15),
transparent 25%
),

radial-gradient(
circle at 50% 80%,
rgba(34,211,238,.12),
transparent 30%
);

animation:ambientGlow 10s ease-in-out infinite;

pointer-events:none;
}

@keyframes gradientBG{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

@keyframes gridMove{
0%{transform:translateY(0);}
100%{transform:translateY(50px);}
}

/* ==========================
   CONTAINER
========================== */

.block-container{
max-width:900px;
padding-top:0.5rem;
padding-bottom:1rem;
position:relative;
z-index:2;
}

/* ==========================
   FLOATING SHIELD
========================== */

.shield{
font-size:90px;
text-align:center;
margin-bottom:5px;

filter:
drop-shadow(0 0 20px #00D4FF)
drop-shadow(0 0 40px #00D4FF);

animation:floatShield 3s ease-in-out infinite;
}

@keyframes floatShield{

0%,100%{
transform:translateY(0);
}

50%{
transform:translateY(-12px);
}

}

/* ==========================
   TITLES
========================== */

.main-title{

text-align:center;

font-size:3.6rem;

font-weight:900;

margin-bottom:5px;

letter-spacing:3px;

/* Animated Neon Gradient */

background:linear-gradient(
90deg,
#00D4FF,
#22D3EE,
#8B5CF6,
#00D4FF
);

background-size:400% 400%;

animation:titleFlow 6s ease infinite;

/* Gradient Text */

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
background-clip:text;

/* Neon Glow */

filter:
drop-shadow(0 0 10px rgba(0,212,255,.8))
drop-shadow(0 0 25px rgba(0,212,255,.5))
drop-shadow(0 0 40px rgba(139,92,246,.4));

}

.sub-title{
text-align:center;
font-size:18px;
color:#CBD5E1;
margin-bottom:30px;
}

/* ==========================
   PREMIUM GLASS CARD
========================== */

.glass-card{

background:rgba(255,255,255,0.06);

backdrop-filter:blur(24px);

border:1px solid rgba(0,212,255,.15);

padding:25px;

border-radius:24px;

box-shadow:
0 0 30px rgba(0,212,255,.15),
inset 0 0 15px rgba(255,255,255,.03);

transition:.4s ease;

}

.glass-card:hover{

transform:translateY(-4px);

box-shadow:
0 0 50px rgba(0,212,255,.30);

}

/* ==========================
   TEXT AREA
========================== */

.stTextArea textarea{

background:rgba(255,255,255,.05)!important;

color:white!important;

border-radius:18px!important;

border:1px solid rgba(255,255,255,.15)!important;

font-size:16px!important;

}

.stTextArea textarea:focus{

border:1px solid #00D4FF!important;

box-shadow:
0 0 20px rgba(0,212,255,.5)!important;

}

/* ==========================
   ANIMATED BUTTON
========================== */

.stButton button{

width:100%;

height:58px;

border:none;

border-radius:16px;

font-size:18px;

font-weight:700;

color:white;

background:linear-gradient(
90deg,
#00D4FF,
#8B5CF6,
#00D4FF
)!important;

background-size:300% 300%!important;

animation:buttonFlow 4s ease infinite;

transition:.3s;
}

.stButton button:hover{

transform:translateY(-3px);

box-shadow:
0 0 30px rgba(0,212,255,.6);

}

@keyframes buttonFlow{

0%{
background-position:0% 50%;
}

50%{
background-position:100% 50%;
}

100%{
background-position:0% 50%;
}

}

@keyframes titleFlow{

0%{
background-position:0% 50%;
}

50%{
background-position:100% 50%;
}

100%{
background-position:0% 50%;
}

}

@keyframes ambientGlow{

0%,100%{
opacity:.8;
}

50%{
opacity:1;
}

}            

/* ==========================
   RESULT CARD
========================== */

.result-card{

padding:20px;

border-radius:18px;

text-align:center;

font-size:22px;

font-weight:700;

margin-top:20px;

}

/* Footer */

.footer{
text-align:center;
margin-top:35px;
color:#94a3b8;
font-size:14px;
}

/* Mobile */

@media(max-width:768px){

.main-title{
font-size:2rem;
}

.sub-title{
font-size:15px;
}

.shield{
font-size:70px;
}

}

</style>
""", unsafe_allow_html=True)

# HEADER
# ==========================

st.markdown(
"""
<div class="main-title">
🛡️ SPAMORA AI
</div>

<div class="sub-title">
Advanced Spam, Scam & Phishing Detection System
</div>
""",
unsafe_allow_html=True
)

# ==========================
# INPUT CARD
# ==========================

st.markdown(
'<div class="glass-card">',
unsafe_allow_html=True
)

message = st.text_area(
    "Enter SMS / Email Message",
    height=220,
    placeholder="Paste your SMS, Email, or suspicious message here..."
)

st.markdown(
'</div>',
unsafe_allow_html=True
)

st.write("")

# ==========================
# ANALYZE BUTTON
# ==========================

# ==========================
# ANALYZE BUTTON
# ==========================

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔍 Scan Message"):

    if not message.strip():

        st.warning("Please enter a message.")

    else:

        with st.spinner("Analyzing message..."):

            processed = transform_text(message)

            vector = tfidf.transform([processed])

            prediction = model.predict(vector)[0]

            # Convert numeric prediction to label
            result = encoder.inverse_transform([prediction])[0]

        # SPAM RESULT
        if "spam" in result.lower() or "phishing" in result.lower():

            st.markdown(
                """
                <div class="result-card"
                style="
                background:#7f1d1d;
                color:white;
                border:1px solid #ef4444;">
                ⚠️ SPAM DETECTED
                </div>
                """,
                unsafe_allow_html=True
            )

        # SAFE RESULT
        else:

            st.markdown(
                """
                <div class="result-card"
                style="
                background:#14532d;
                color:white;
                border:1px solid #22c55e;">
                ✅ NO SPAM DETECTED
                </div>
                """,
                unsafe_allow_html=True
            )
# ==========================
# FOOTER
# ==========================

st.markdown(
"""
<div class="footer">
Powered by Spamora AI • AI Based Cybersecurity Protection
</div>
""",
unsafe_allow_html=True
)
