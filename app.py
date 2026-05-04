import streamlit as st
from src.recommender import load_songs, recommend_songs
from src.rag_assistant import RagAssistant
from src.guardrails import check_unsupported_query, calculate_confidence, check_recommendation_quality
from src.main import parse_query_to_prefs

# Load data only once
@st.cache_data
def get_data():
    songs = load_songs("data/songs.csv")
    assistant = RagAssistant("data/knowledge_base.txt")
    return songs, assistant

st.set_page_config(page_title="Music AI Assistant", page_icon="🎵")

st.title("🎵 Music Discovery AI Assistant")
st.write("Ask me for music recommendations! (e.g., *'Recommend chill songs for studying'* or *'I want high-energy pop songs for the gym'*).")

songs, assistant = get_data()

query = st.text_input("What kind of music are you looking for?")

if st.button("Get Recommendations"):
    if not query:
        st.warning("Please enter a query.")
    else:
        # Guardrail Check
        is_supported, warning = check_unsupported_query(query)
        if not is_supported:
            st.error(f"⚠️ Guardrail Blocked: {warning}")
        else:
            with st.spinner("Analyzing request..."):
                prefs = parse_query_to_prefs(query)
                context = assistant.retrieve(query, top_k=2)
                recommendations = recommend_songs(prefs, songs, k=3)
                confidence = calculate_confidence(recommendations)
                
                is_good_quality, quality_warning = check_recommendation_quality(recommendations)
                
                if not is_good_quality:
                    st.warning(f"⚠️ {quality_warning}")
                
                st.subheader("Your Recommendations")
                
                if recommendations:
                    for i, (song, score, explanation) in enumerate(recommendations, 1):
                        st.markdown(f"**{i}. {song['title']} by {song['artist']}**")
                        st.markdown(f"**Score:** `{score:.2f}`")
                        st.markdown(f"**Reason:** *{explanation}*")
                        st.markdown("---")
                else:
                    st.info("No recommendations found.")

                st.subheader("Assistant Confidence & Knowledge Base Context")
                st.metric("Confidence Score", f"{confidence:.2f} / 1.00")
                
                if context:
                    with st.expander("Why these recommendations?"):
                        for c in context:
                            st.write(f"- {c}")
