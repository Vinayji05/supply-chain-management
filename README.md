# SCM Simulator

## Build (Windows/Linux)

1. Build C++ simulator:
   g++ -O2 -std=c++17 -o src/simulator/simulate src/simulator/main.cpp

2. Create Python env and install dependencies:
   pip install -r requirements.txt

3. Run Streamlit app:
   streamlit run streamlit_app/app.py

The Streamlit app calls the C++ simulator executable; ensure the `simulate` binary path is set in the app UI.

A Dockerfile is included to build a container with both the C++ binary and Streamlit app.
