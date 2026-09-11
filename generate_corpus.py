import json
import random

memes = [
    {
        "meme_id": "MEME_001",
        "title": "Dashamoolam Damu Police Station Breakdown",
        "character": "Dashamoolam Damu",
        "movie": "Chattambinadu",
        "raw_ocr_text": "Dashamoolam Damu: Athu pinne sir... njan oru simple quotation eduthatha! Sadhanam kayyilundo mwone?! HAHAHA AYYO SCENE! Salim Kumar reaction epic!",
        "year": 2009,
        "category": "Classic Quotation"
    },
    {
        "meme_id": "MEME_002",
        "title": "KTU BTech Supplementary Exam Depression",
        "character": "Distressed Engineering Student",
        "movie": "Real Life Kerala",
        "raw_ocr_text": "KTU supply result vannu eda! 5 supply koodi kitti... Entho chiri varunnu haha! Ini enthu cheyyum? Porotta and beef thinnu hartal aagoshikkam!",
        "year": 2023,
        "category": "KTU Trauma"
    },
    {
        "meme_id": "MEME_003",
        "title": "Manavalan and Sons Dubai Enterprise",
        "character": "Manavalan",
        "movie": "Pulival Kalyanam",
        "raw_ocr_text": "Manavalan: Ente company Manavalan and Sons Dubai branch-il chaya and porotta supplies illathe poyi! Adipoli mwone!! Theppu kitto entho hehehe?!",
        "year": 2003,
        "category": "Entrepreneurship"
    },
    {
        "meme_id": "MEME_004",
        "title": "Ramanathan in Punjabi House Well",
        "character": "Ramanathan & Gangadharan",
        "movie": "Punjabi House",
        "raw_ocr_text": "Harisree Ashokan as Ramanathan: Ayyo Gangadharan ammavaney! Kinaril chadi chathu ennu parayilla! CID Moosa entry pole CID level scene haha!!",
        "year": 1998,
        "category": "Slapstick Tragedy"
    },
    {
        "meme_id": "MEME_005",
        "title": "Jagathy Arumugham Linguistic Masterclass",
        "character": "Jagathy Sreekumar",
        "movie": "Yodha",
        "raw_ocr_text": "Jagathy: Kutti mama njan pottan alla! Ashokettan adipoli scene. Chalu comedy parayalle mwone, sadhanam ready aayi! HEHEHE ENTHINA EDA CHIRI?!",
        "year": 1992,
        "category": "Linguistic Gold"
    },
    {
        "meme_id": "MEME_006",
        "title": "Sudhi and CID Moosa Dog Squad Debacle",
        "character": "CID Moosa",
        "movie": "CID Moosa",
        "raw_ocr_text": "CID Moosa: Arjun, attack! Pinarayi sarkarinte hartal divasam kambi and porotta vangan poya CID Moosa police dog fail aayi! Hahaha ayyo!",
        "year": 2003,
        "category": "Investigation Comedy"
    },
    {
        "meme_id": "MEME_007",
        "title": "Pinarayi Press Conference Punchlines",
        "character": "Political Hivemind",
        "movie": "Kerala News Cycle",
        "raw_ocr_text": "Pinarayi vijayan: Kadakku purathu! Congress and BJP opposition chalu irakki scene aakkunnu. Nale hartal aano mwone? Beef fry ready aayi!",
        "year": 2021,
        "category": "Political Satire"
    },
    {
        "meme_id": "MEME_008",
        "title": "Theppu at Marine Drive Kochi",
        "character": "Heartbroken Lover",
        "movie": "Premam Nostalgia",
        "raw_ocr_text": "Avasanam aval theppu thannu poyi mwone... Marine drive-il irunnu chaya kudichu karayunnu. Harisree Ramanathan pole life scene aayi! AYYO ENTHINA?!",
        "year": 2015,
        "category": "Tragic Romance"
    },
    {
        "meme_id": "MEME_009",
        "title": "Salim Kumar Pyari Sleep Deprivation",
        "character": "Pyari",
        "movie": "Kalyanaraman",
        "raw_ocr_text": "Salim kumar as Pyari: Njan urangittilla sir! Dashamoolam damu-vine kandappol chirichu chathu haha hehe! Sadhanam kayyil illekilum scene adipoli!",
        "year": 2002,
        "category": "Workplace Satire"
    },
    {
        "meme_id": "MEME_010",
        "title": "Kerala Midnight Thattukada Vibe",
        "character": "Night Owl Foodies",
        "movie": "Kochi Night Life",
        "raw_ocr_text": "Midnight 2 AM thattukada: Porotta, double beef fry, pinne oru strong chaya. KTU supply marakkan ithilum nalla sadhanam vere undo mwone?! ADIPOLI SCENE!",
        "year": 2024,
        "category": "Gastronomic Bliss"
    }
]

# Expand to reach ~40 KB payload as celebrated in the prompt
corpus = []
for i in range(85):
    base = memes[i % len(memes)]
    item = dict(base)
    item["meme_id"] = f"MEME_{i+1:03d}"
    item["engagement_score"] = round(random.uniform(500, 95000), 2)
    item["shares_count"] = random.randint(50, 12000)
    item["troll_page_handle"] = f"@troll_malayalam_node_{i%12}"
    item["cloud_distributed_shard_id"] = f"shard_asia_south_kerala_{i%4}"
    corpus.append(item)

payload = json.dumps(corpus, indent=4, ensure_ascii=False)
with open("meme_corpus.json", "w", encoding="utf-8") as f:
    f.write(payload)

size_kb = len(payload.encode("utf-8")) / 1024
print(f"Generated meme_corpus.json with {len(corpus)} records, payload size: {size_kb:.2f} KB")
