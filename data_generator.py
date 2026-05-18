import random
import csv

DISASTER_TYPES=['FIRE', 'FLOOD', 'FOREST_FIRE']
DISTRICTS= ['Kailali', 'Bardiya', 'Dang', 'Surkhet', 'Banke', 'Dolpa', 'Jumla', 'Rukum', 'Salyan', 'Rolpa']

def compute_label(disaster_type, severity, road_blocked):
    base = severity // 2 #base for severity, floor division by 2 (eg 11/5.5 xa vane 5)
    if road_blocked:
        base += 2 #if road is blocked adding 2 to the base
    if disaster_type == 'FIRE':
        base +=1 
    elif disaster_type == 'FLOOD':
        base +=2 
    elif disaster_type == 'FOREST_FIRE':
        base +=1
    return min(base, 8) #max label 8 hunxa mathi jana painna 

def generate_dataset(num_records=500):
    records = []
    for _ in range(num_records):
        disaster_type = random.choice(DISASTER_TYPES)
        severity = random.randint(1,10)
        road_blocked = random.randint(0,1)
        district = random.choice(DISTRICTS)
        recommended_resources = compute_label(disaster_type, severity, road_blocked)
        records.append({
            "disaster_type": disaster_type,
            "severity": severity,
            "road_blocked": road_blocked,
            "district": district,
            "recommended_resources": recommended_resources
        })
    return records

def save_csv(records, filename='disaster_dataset.csv'):
    keys= ["disaster_type","severity", "road_blocked", "district", "recommended_resources"]
    with open(filename,"w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)
    print(f"Dataset saved: {len(records)} records to {filename}")
if __name__ == "__main__":
    records = generate_dataset(500)
    save_csv(records)
