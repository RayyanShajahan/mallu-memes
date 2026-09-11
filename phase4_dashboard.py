import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os

class KeralaMoodIndexDashboard:
    """
    Hyper-converged, zero-latency visualization matrix to project the 
    Kerala collective consciousness into ocular space using Streamlit.
    """

    def __init__(self, data_path="mood_indexed_memes.json"):
        self.data_path = data_path
        # Force maximum aesthetic pretentiousness
        st.set_page_config(page_title="KMI Telemetry", layout="wide", page_icon="🌴")

    def _load_payload(self):
        """Simulate a high-throughput connection to our mock-Elasticsearch JSON node."""
        if not os.path.exists(self.data_path):
            st.error(f"[FATAL EXCEPTION] Data plane missing. Execute Phase 3 to generate {self.data_path}.")
            st.stop()
        
        with open(self.data_path, "r", encoding="utf-8") as f:
            return pd.DataFrame(json.load(f))

    def render(self):
        st.markdown("<h1 style='text-align: center;'>🌴 The 'Meme-ing of Life' Sentiment Analyzer</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #ff4b4b;'>Kerala Existential Telemetry & Mood Index (KMI)</h4>", unsafe_allow_html=True)
        st.divider()

        df = self._load_payload()
        
        # Calculate the absolute median state of the state
        global_kmi = df["kerala_mood_index"].mean()
        dominant_state = df["dominant_mood"].mode()[0]

        # Row 1: Flashy Gauges
        col1, col2 = st.columns(2)
        
        with col1:
            # Over-engineered Plotly Gauge
            fig_kmi = go.Figure(go.Indicator(
                mode="gauge+number",
                value=global_kmi,
                title={'text': "Aggregate Kerala Mood Index (KMI)", 'font': {'size': 24}},
                gauge={
                    'axis': {'range': [0, 15], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#ff4b4b"},
                    'steps': [
                        {'range': [0, 5], 'color': "#1a1a1a"},
                        {'range': [5, 10], 'color': "#333333"},
                        {'range': [10, 15], 'color': "#4d4d4d"}
                    ],
                    'threshold': {
                        'line': {'color': "cyan", 'width': 4},
                        'thickness': 0.75,
                        'value': 12
                    }
                }
            ))
            fig_kmi.update_layout(height=400, template="plotly_dark")
            st.plotly_chart(fig_kmi, use_container_width=True)

        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.metric(label="Current Prevailing Psyche", value=dominant_state, delta="-20% Sanity", delta_color="inverse")
            st.metric(label="Meme Artifacts Processed", value=len(df), delta="+500 Shokam")
            st.caption("Data aggregated via distributed PySpark pipeline and Vernacular NLP parsing.")

        st.divider()

        # Row 2: Deep Analytics
        st.subheader("Sub-Symbolic Semantic Distribution")
        col3, col4 = st.columns([2, 1])

        with col3:
            # Multi-dimensional mood mapping
            mood_counts = df["dominant_mood"].value_counts().reset_index()
            mood_counts.columns = ["Mood Category", "Volume"]
            fig_bar = px.bar(
                mood_counts, 
                x="Volume", 
                y="Mood Category", 
                orientation='h', 
                color="Volume", 
                color_continuous_scale="Reds",
                title="Affective Psychometric Volume"
            )
            fig_bar.update_layout(template="plotly_dark")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col4:
            st.dataframe(
                df[["title", "kerala_mood_index"]].sort_values(by="kerala_mood_index", ascending=False).head(8),
                use_container_width=True,
                hide_index=True
            )
            st.caption("Top Existentially Heavy Artifacts")

if __name__ == "__main__":
    app = KeralaMoodIndexDashboard()
    app.render()
