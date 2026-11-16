import json

def audit():
    with open("backend/evaluation_results.json", "r") as f:
        data = json.load(f)
        
    scenarios = data.get("scenarios", [])
    metrics = data.get("metrics", {})
    
    print(f"Total scenarios in file: {len(scenarios)}")
    print(f"Reported metrics block: {metrics}")
    
    actual_pass = [s for s in scenarios if s.get("status") == "PASS"]
    actual_fail = [s for s in scenarios if s.get("status") == "FAIL"]
    
    print(f"Computed PASS: {len(actual_pass)}, Computed FAIL: {len(actual_fail)}")
    
    print("\n--- Failed Scenarios ---")
    for s in actual_fail:
        print(f"ID: {s['id']} | Category: {s['category']} | Desc: {s['description']}")
        print(f"  Expected: {s['expected']}")
        print(f"  Notes: {s['notes']}")
        
    print("\n--- Scenarios that used Fallback or AI ---")
    for s in scenarios:
        notes = s.get("notes", "")
        if "Fallback" in notes or "fallback" in notes or "Gemini" in notes:
            print(f"ID: {s['id']} | Status: {s['status']} | Notes: {notes}")

if __name__ == "__main__":
    audit()
