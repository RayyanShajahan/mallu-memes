import os
import re

# Auto-detect JAVA_HOME if not loaded into the current terminal session
if "JAVA_HOME" not in os.environ:
    common_jdk_paths = [
        r"C:\Program Files\Microsoft\jdk-17.0.20.101-hotspot",
        r"C:\Program Files\Eclipse Adoptium\jdk-17",
        r"C:\Program Files\Java\jdk-17"
    ]
    for jdk_path in common_jdk_paths:
        if os.path.isdir(jdk_path):
            os.environ["JAVA_HOME"] = jdk_path
            os.environ["PATH"] = os.path.join(jdk_path, "bin") + os.pathsep + os.environ.get("PATH", "")
            break

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, when, length
from pyspark.sql.types import FloatType, IntegerType, StringType

class KeralaDistributedMemeComputeEngine:
    """
    Enterprise-grade distributed processing framework to compute 
    existential metrics from vernacular meme artifacts.
    """

    def __init__(self, app_name="KeralaCollectivePsycheDistributedProcessor"):
        # Initializing distributed cluster resources on a single laptop core
        print("[INIT] Allocating hyper-converged Spark execution nodes...")
        self.spark = (
            SparkSession.builder
            .appName(app_name)
            .master("local[*]")
            .config("spark.driver.memory", "2g")
            .config("spark.sql.shuffle.partitions", "2")
            .getOrCreate()
        )
        # Suppress verbose JVM log vomit
        self.spark.sparkContext.setLogLevel("ERROR")

    @staticmethod
    def _compute_cultural_relevance(text: str) -> float:
        """
        Calculates Cultural Relevance (0.0 to 10.0) based on sacred 
        Malayalam cinema tropes, Mohanlal/Mammootty archetypes, and KTU trauma.
        """
        if not text:
            return 0.0

        lowered = text.lower()

        # Sacred anchor vocabulary for the Mallu hivemind
        cultural_anchors = {
            "damu": 2.5, "dashamoolam": 3.0, "manavalan": 2.5, "salim kumar": 3.0,
            "jagathy": 3.0, "harisree": 2.0, "ramanathan": 2.0, "cid moosa": 2.5,
            "theppu": 2.0, "scene": 1.5, "mwone": 1.5, "adipoli": 1.0,
            "porotta": 1.5, "beef": 1.5, "chaya": 1.0, "hartal": 2.0,
            "ktu": 3.0, "supply": 2.5, "pinarayi": 2.0, "bjp": 1.5,
            "congress": 1.5, "kambi": 1.0, "chalu": 1.5, "sadhanam": 2.0
        }

        score = sum(weight for anchor, weight in cultural_anchors.items() if anchor in lowered)
        
        # Normalize arbitrarily to cap at 10.0 for scientific credibility
        return min(round(float(score), 2), 10.0)

    @staticmethod
    def _compute_humor_density(text: str) -> float:
        """
        Calculates Humor Density (0.0 to 10.0) using non-linear heuristic analysis
        of punctuational hysteria, Manglish laughter, and all-caps rage.
        """
        if not text:
            return 0.0

        score = 1.0
        # Metric 1: Excessive punctuation denotes heightened comedic distress
        punc_count = len(re.findall(r'[!?.]', text))
        score += min(punc_count * 0.4, 3.0)

        # Metric 2: Manglish chuckles and phonetic laughter
        laugh_patterns = re.findall(r'(haha|hehe|chiri|eda|entho|ayyo|enthina)', text.lower())
        score += min(len(laugh_patterns) * 1.5, 4.0)

        # Metric 3: Ratio of shouty upper-case energy
        caps_count = sum(1 for c in text if c.isupper())
        if len(text) > 0 and (caps_count / len(text)) > 0.3:
            score += 2.0

        return min(round(float(score), 2), 10.0)

    def run_etl(self, input_path="meme_corpus.json", output_path="processed_memes.json"):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"[ABORT] Cannot locate {input_path}. Did Phase 1 complete successfully?")

        print(f"[STAGE 1] Ingesting schema from distributed storage abstraction: {input_path}")
        df = self.spark.read.option("multiline", "true").json(input_path)

        # Register vectorized UDFs to convince onlookers this couldn't be done in pandas
        cultural_udf = udf(self._compute_cultural_relevance, FloatType())
        humor_udf = udf(self._compute_humor_density, FloatType())

        print("[STAGE 2] Executing distributed matrix transformations across worker threads...")
        processed_df = (
            df
            .withColumn("cultural_relevance_index", cultural_udf(col("raw_ocr_text")))
            .withColumn("humor_density_metric", humor_udf(col("raw_ocr_text")))
            # Compound tensor index: Harmonic synthesis of satire and nostalgia
            .withColumn(
                "kerala_existential_weight",
                (col("cultural_relevance_index") * 0.6) + (col("humor_density_metric") * 0.4)
            )
        )

        print("[STAGE 3] Collecting distributed partitions into low-latency analytical payload...")
        # Convert Spark DataFrame back to local JSON for zero-infrastructure frontend ingestion
        records = [row.asDict() for row in processed_df.collect()]

        import json
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=4)

        print(f"[SUCCESS] Distributed computation resolved. Persisted {len(records)} transformed records to {output_path}.")
        self.spark.stop()

if __name__ == "__main__":
    engine = KeralaDistributedMemeComputeEngine()
    engine.run_etl()
