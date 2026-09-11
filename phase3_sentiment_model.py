import json
import os
import re
from datetime import datetime

class VernacularPsycheNLPEngine:
    """
    Sub-symbolic semantic decomposition engine designed to map chaotic 
    Manglish utterances and Malayalam pop-culture distress into discrete 
    affective psychometric buckets.
    """

    def __init__(self, input_path="processed_memes.json", output_path="mood_indexed_memes.json"):
        self.input_path = input_path
        self.output_path = output_path

        # Semantic anchor taxonomy for Malayalam cultural anxieties
        self.mood_taxonomies = {
            "KTU Exam Trauma": [
                "ktu", "supply", "exam", "tholi", "fail", "paditham", 
                "btech", "assignment", "series", "arrear", "internal"
            ],
            "Monday Work Shokam": [
                "monday", "work", "office", "manager", "urakkam", "leave", 
                "madi", "pani", "salary", "appraisal", "login"
            ],
            "Political Poru & Hartal": [
                "pinarayi", "bjp", "congress", "cpim", "hartal", "kodi", 
                "strike", "nethavu", "sarkar", "election", "charcha"
            ],
            "Theppu & Romantic Melodrama": [
                "theppu", "snehichu", "kaamuki", "kamukan", "breakup", 
                "sad", "thech", "kalyanam", "single", "crush"
            ],
            "Nirvana (Thattukada & Vibe)": [
                "porotta", "beef", "chaya", "adipoli", "vibe", "scene", 
                "kidu", "set", "food", "koottukaran"
            ],
            "Existential Nihilism": [
                "shokam", "veruppikkaal", "daridryam", "oola", "myr", 
                "enthina", "jeevitham", "bore", "nashttam", "chalu"
            ]
        }

    def _tokenize(self, text: str) -> list[str]:
        """Low-latency vernacular tokenizer stripping noise and punctuation."""
        if not text:
            return []
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        return cleaned.split()

    def _classify_sentiment_vector(self, tokens: list[str]) -> dict:
        """Calculates multi-class sentiment vector distribution."""
        vector = {category: 0 for category in self.mood_taxonomies}
        
        for token in tokens:
            for category, lexicon in self.mood_taxonomies.items():
                if token in lexicon:
                    vector[category] += 1

        total_hits = sum(vector.values())
        dominant_mood = max(vector, key=vector.get) if total_hits > 0 else "Neutral Stoicism"
        
        # Confidence normalization
        confidence = round((vector[dominant_mood] / total_hits), 2) if total_hits > 0 else 0.50

        return {
            "dominant_mood": dominant_mood,
            "vector": vector,
            "classification_confidence": confidence
        }

    def run_pipeline(self):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"[HALT] Cannot locate {self.input_path}. Run Phase 2 first!")

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Ingesting PySpark analytical matrix: {self.input_path}")
        with open(self.input_path, "r", encoding="utf-8") as f:
            memes = json.load(f)

        mood_distribution = {}

        for meme in memes:
            tokens = self._tokenize(meme.get("raw_ocr_text", ""))
            sentiment_meta = self._classify_sentiment_vector(tokens)

            meme["dominant_mood"] = sentiment_meta["dominant_mood"]
            meme["sentiment_vector"] = sentiment_meta["vector"]
            meme["mood_confidence"] = sentiment_meta["classification_confidence"]

            # Compute Kerala Mood Index (KMI):
            # Harmonic interplay between Existential Weight and NLP Confidence
            kew = meme.get("kerala_existential_weight", 5.0)
            conf_multiplier = 1.0 + (sentiment_meta["classification_confidence"] * 0.5)
            meme["kerala_mood_index"] = round(min(kew * conf_multiplier, 15.0), 2)

            mood_distribution[meme["dominant_mood"]] = mood_distribution.get(meme["dominant_mood"], 0) + 1

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(memes, f, ensure_ascii=False, indent=4)

        print(f"[SUCCESS] Classified {len(memes)} vernacular items. Output persisted to {self.output_path}")
        print("\n=== KERALA COLLECTIVE MOOD MATRIX ===")
        for mood, count in sorted(mood_distribution.items(), key=lambda x: x[1], reverse=True):
            print(f"  * {mood:<32} : {count} memes")

if __name__ == "__main__":
    classifier = VernacularPsycheNLPEngine()
    classifier.run_pipeline()
