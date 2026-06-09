
from collections import Counter
import re

from database import SessionLocal, engine
from models import SecurityLog, Base

Base.metadata.create_all(bind=engine)

LOG_FILE = "logs/sample.log"

db = SessionLocal()

ips = []

with open(LOG_FILE) as file:
    for line in file:
        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
        if not match:
            continue
        ips.append(match.group(1))

count = Counter(ips)

for ip, attempts in count.items():
    if attempts >= 3:
        db.add(SecurityLog(
            ip=ip,
            threat="Brute Force",
            severity="High"
        ))

db.commit()
print("Threats saved")
