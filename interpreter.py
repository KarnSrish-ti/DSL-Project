#interpreter.py 

from pyexpat import features

import joblib 
import numpy as np

# model and encoders load
model= joblib.load('dispatch_model.joblib')
le_disaster = joblib.load('le_disaster.joblib')
le_district = joblib.load('le_district.joblib')

#simulation state 
environment ={
    'incidents':[],
    'resources':{},
    'roads':{}, 
    'alerts':[],
    'rules': []
}

def predict_resources(disaster_type, severity, district):

    road_blocked = 0

    for (from_d, to_d), status in environment["roads"].items():
        if to_d == district or from_d == district:
            if status == "blocked":
                road_blocked = 1
                break

    try:
        disaster_enc = le_disaster.transform([disaster_type])[0]
    except ValueError:
        disaster_enc = 0

    try:
        district_enc = le_district.transform([district])[0]
    except ValueError:
        district_enc = 0

    features = np.array([[disaster_enc, severity, road_blocked, district_enc]])

    prediction = model.predict(features)[0]

    return round(prediction), road_blocked
def execute(ast):
    for node in ast:
        node_type = node["type"]

        if node_type == "INCIDENT":
            disaster = node["disaster"]
            district = node["district"]
            severity = node["severity"]
            recommended, road_blocked = predict_resources(disaster, severity, district)
            environment["incidents"].append({
                "disaster": disaster,
                "district": district,
                "severity": severity,
                "road_blocked": road_blocked,
                "ml_recommended_resources": recommended
            })
        elif node_type == "ALLOCATE":
            district = node["district"]
            resource = node["resource"]
            quantity = node["quantity"]
            if district not in environment["resources"]:
                environment["resources"][district] = {}
            environment["resources"][district][resource] = quantity

        elif node_type == "DISPATCH_RULE":
            environment["rules"].append({
                "threshold": node["threshold"],
                "team": node["team"]
            })

        elif node_type == "ROAD_UPDATE":
            key = (node["from_district"], node["to_district"])
            environment["roads"][key] = node["status"]

        elif node_type == "ALERT":
            environment["alerts"].append({
                "condition": f"{node['condition_var']} > {node['threshold']}",
                "message": node["message"],
                "target": node["target"]
            })

def print_report():
    print("\n DISPATCHLANG SIMULATION REPORT \n")

    print(" INCIDENTS ")
    if not environment["incidents"]:
        print("  None")
    for inc in environment["incidents"]:
        blocked = "YES" if inc["road_blocked"] else "NO"
        print(f"  [{inc['disaster']}] {inc['district']} | Severity: {inc['severity']} | Road Blocked: {blocked} | ML Recommended Resources: {inc['ml_recommended_resources']}")

    print("\nRESOURCES ALLOCATED ")
    if not environment["resources"]:
        print("  None")
    for district, res in environment["resources"].items():
        for resource, qty in res.items():
            print(f"  {district} ← {qty} {resource}")

    print("\n ROAD STATUS ")
    if not environment["roads"]:
        print("  None")
    for (f, t), status in environment["roads"].items():
        print(f"  {f} → {t} : {status.upper()}")

    print("\n DISPATCH RULES ")
    if not environment["rules"]:
        print("  None")
    for rule in environment["rules"]:
        print(f"  IF severity > {rule['threshold']} THEN dispatch {rule['team']}")

    print("\nALERTS ")
    if not environment["alerts"]:
        print("  None")
    for alert in environment["alerts"]:
        print(f"  WHEN {alert['condition']} → SEND {alert['message']} TO {alert['target']}")