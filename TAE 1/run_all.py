import subprocess
import os
import time
import sys

def run():
    print("-" * 50)
    print("🚀 ENGINEERING HOSPITAL SYSTEM - UNIFIED LAUNCHER")
    print("-" * 50)
    
    # 1. Start Backend
    print("\n👉 Starting Flask Backend (on http://localhost:5000)...")
    backend_process = subprocess.Popen([sys.executable, "backend/app.py"], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.STDOUT, 
                                      text=True, 
                                      bufsize=1,
                                      shell=True)
    
    # Wait for backend to be ready
    time.sleep(3)
    
    # 2. Start Frontend
    print("👉 Starting React Frontend (on http://localhost:5173)...")
    frontend_process = subprocess.Popen("npm run dev", 
                                       cwd="frontend", 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.STDOUT, 
                                       text=True, 
                                       bufsize=1,
                                       shell=True)
    
    print("\n✅ BOTH SERVERS ARE RUNNING!")
    print("🌍 Open your browser to: http://localhost:5173")
    print("-" * 50)
    print("Press Ctrl+C to stop the system.")
    print("-" * 50)

    try:
        while True:
            # Check if processes are still alive
            if backend_process.poll() is not None:
                print("\n❌ Backend stopped unexpectedly.")
                break
            if frontend_process.poll() is not None:
                print("\n❌ Frontend stopped unexpectedly.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Done.")

if __name__ == "__main__":
    run()
