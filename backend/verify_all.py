import time
import subprocess
import requests

def verify_all():
    print("--- STEP 1: Starting Backend & Frontend ---")
    be_proc = subprocess.Popen(
        ["python", "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8001"],
        cwd="e:\\MatchMyResume\\backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    fe_proc = subprocess.Popen(
        ["cmd.exe", "/c", "npm run dev -- --port 5173 --host 127.0.0.1"],
        cwd="e:\\MatchMyResume\\frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(5)

    try:
        # Check backend
        print("\n--- STEP 2: Checking Backend Health ---")
        be_res = requests.get("http://127.0.0.1:8001/api/health", timeout=5)
        print("Backend Status:", be_res.status_code, be_res.json())
        assert be_res.status_code == 200

        # Check frontend
        print("\n--- STEP 3: Checking Frontend Landing Page ---")
        fe_res = requests.get("http://127.0.0.1:5173/", timeout=5)
        print("Frontend Status:", fe_res.status_code)
        assert fe_res.status_code == 200
        content = fe_res.text

        # Verify no fake sample analysis
        assert "Sample Analysis: Senior Full-Stack Engineer" not in content
        assert "Live Mock Data" not in content
        print("Verified: Sample Analysis section is completely removed!")

        # Verify technical stack jargon is not in public HTML
        assert "PyMuPDF Engine" not in content
        assert "Scikit-Learn TF-IDF" not in content
        print("Verified: Public technical stack jargon removed!")

        print("\n--- STEP 4: Checking All Protected Routes via Frontend ---")
        for route in ["/", "/analyze", "/dashboard", "/insights"]:
            r = requests.get(f"http://127.0.0.1:5173{route}", timeout=5)
            print(f"Route {route} -> Status: {r.status_code}")
            assert r.status_code == 200

        print("\nALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")

    finally:
        be_proc.terminate()
        fe_proc.terminate()
        be_proc.wait()
        fe_proc.wait()

if __name__ == "__main__":
    verify_all()
