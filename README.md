# Rubik’s Cube Solver GUI

**Interactive Python Rubik’s Cube solver** with a Tkinter GUI, integrating **Kociemba’s Two-Phase Algorithm** for optimal (≤20-move) solutions. Features scramble generation, manual algorithm input, real-time animation, adjustable speed, accurate internal state tracking, and easy extensibility (2×2, 4×4, etc.).

---

## 🚀 Features

- Optimal solving via **Kociemba’s Two-Phase Algorithm**  
- Interactive **Tkinter GUI**: scramble, solve, reset, manual moves  
- Real-time animated solving with adjustable speed  
- Cube state modeled with **NumPy arrays**  
- Manual algorithm entry (e.g., `R U R' U'`)  
- Scramble reproducibility & move history  
- Designed for scalability to other cube sizes  

---

## 🧰 Prerequisites (everything needed before running)

1. **Git**  
   - Install from: https://git-scm.com/downloads  
   - Verify:  
     ```bash
     git --version
     ```

2. **Python 3.11 (64-bit recommended)**  
   - Download: https://www.python.org/downloads/release/python-311/  
   - During Windows install: check **"Add Python to PATH"**.  
   - Verify:  
     ```bash
     python --version
     ```

3. **pip** (bundled with Python)  
   - Upgrade to latest:  
     ```bash
     python -m pip install --upgrade pip
     ```

4. **(Windows only)** Microsoft Visual C++ Build Tools  
   - Only required if `kociemba` falls back to source build and errors out.  
   - Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/  
   - Install the **"Desktop development with C++"** workload.

---

## 📦 Installation & Setup (cross-platform)

### 1. Clone repository
```bash
git clone https://github.com/<your-username>/rubiks-cube-solver-gui.git
cd rubiks-cube-solver-gui



### 2. Create and activate virtual environment
Windows (PowerShell):
py -3.11 -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process  # only if blocked
.\.venv\Scripts\Activate.ps1

Windows (CMD):
py -3.11 -m venv .venv
.\.venv\Scripts\activate.bat

macOS / Linux:
python3.11 -m venv .venv
source .venv/bin/activate

After activation your prompt should show (.venv).

### 3. Upgrade packaging tools
python -m pip install --upgrade pip setuptools wheel

### 4. Install dependencies
Preferred (if file exists):
python -m pip install -r requirements.txt
Or
explicitly:
python -m pip install numpy kociemba
Windows tip: If kociemba fails during install with compiler errors, install Visual C++ Build Tools and retry:
python -m pip install --upgrade pip setuptools wheel
python -m pip install kociemba

▶ Running the Solver
Ensure the virtual environment is active, then execute:
python rubiks_cube_solver.py

The Tkinter GUI will launch.

#### GUI Controls Overview :
Scramble: Applies a random scramble to the cube.

Solve: Calls Kociemba solver on current cube state and animates the returned optimized move sequence.

Reset: Returns cube to solved state.

Run Algo: Manually enter any algorithm (e.g., R U R' U') to apply.

Speed slider: Adjust animation delay for clarity or speed.

#### Internal Mechanics Summary:
Cube stored as six 3×3 NumPy arrays for faces (U, D, F, B, L, R).

Colors mapped to solver faces (W→U, Y→D, G→F, B→B, O→L, R→R).

cube.to_kociemba_string() produces the 54-character facelet string.

kociemba.solve(...) computes optimal sequence.

Custom move engine applies each move and updates GUI in real time.

🛠 Troubleshooting
Missing module errors :

python -m pip install numpy kociemba
kociemba build failure on Windows
Install Visual C++ Build Tools and retry installation. Use Python 3.11 for best wheel support.
Recommended Repository Layout
Cube not solved after animation

Check scramble string and solver output in GUI.

Log facelet string input to Kociemba for debugging.
