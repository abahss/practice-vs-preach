import requests, os
import BundestagsAPy
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")

client = BundestagsAPy.Client(API_KEY)

protocols = client.bt_plenarprotokoll(
    start_date="2025-01-01",
    end_date="2025-12-01",
    max_results=False
)

for p in protocols:
    doc = client.bt_plenarprotokoll_text(id=p.id, max_results=1, format="xml")
    breakpoint()
    with open(f"tmp/plenar_xml/{pid}.xml", "wb") as f:
        f.write(doc.raw)

