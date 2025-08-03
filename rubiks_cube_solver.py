import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

try:
    import kociemba
    KOCIEMBA_AVAILABLE = True
except ImportError:
    KOCIEMBA_AVAILABLE = False


class RubiksCube:
    def __init__(self):
        self.faces = {
            'U': np.full((3, 3), 'W', dtype=str),
            'D': np.full((3, 3), 'Y', dtype=str),
            'F': np.full((3, 3), 'G', dtype=str),
            'B': np.full((3, 3), 'B', dtype=str),
            'L': np.full((3, 3), 'O', dtype=str),
            'R': np.full((3, 3), 'R', dtype=str)
        }
        self.move_history = []
        self.last_scramble = []

    def is_solved(self):
        for face in self.faces:
            center = self.faces[face][1, 1]
            if not np.all(self.faces[face] == center):
                return False
        return True

    def to_kociemba_string(self):
        color_to_face = {'W': 'U', 'Y': 'D', 'G': 'F', 'B': 'B', 'O': 'L', 'R': 'R'}
        order = ['U', 'R', 'F', 'D', 'L', 'B']
        facelets = []
        for f in order:
            for i in range(3):
                for j in range(3):
                    facelets.append(color_to_face[self.faces[f][i, j]])
        return ''.join(facelets)

    def rotate_face_clockwise(self, face):
        self.faces[face] = np.rot90(self.faces[face], k=-1)

    def rotate_face_counter_clockwise(self, face):
        self.faces[face] = np.rot90(self.faces[face], k=1)

    # Basic face moves
    def move_U(self):
        self.rotate_face_clockwise('U')
        temp = self.faces['F'][0].copy()
        self.faces['F'][0] = self.faces['R'][0]
        self.faces['R'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['L'][0]
        self.faces['L'][0] = temp
        self.move_history.append("U")

    def move_U_prime(self):
        self.rotate_face_counter_clockwise('U')
        temp = self.faces['F'][0].copy()
        self.faces['F'][0] = self.faces['L'][0]
        self.faces['L'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['R'][0]
        self.faces['R'][0] = temp
        self.move_history.append("U'")

    def move_D(self):
        self.rotate_face_clockwise('D')
        temp = self.faces['F'][2].copy()
        self.faces['F'][2] = self.faces['L'][2]
        self.faces['L'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['R'][2]
        self.faces['R'][2] = temp
        self.move_history.append("D")

    def move_D_prime(self):
        self.rotate_face_counter_clockwise('D')
        temp = self.faces['F'][2].copy()
        self.faces['F'][2] = self.faces['R'][2]
        self.faces['R'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['L'][2]
        self.faces['L'][2] = temp
        self.move_history.append("D'")

    def move_R(self):
        self.rotate_face_clockwise('R')
        temp = np.array([self.faces['F'][i][2] for i in range(3)])
        for i in range(3):
            self.faces['F'][i][2] = self.faces['D'][i][2]
            self.faces['D'][i][2] = self.faces['B'][2 - i][0]
            self.faces['B'][2 - i][0] = self.faces['U'][i][2]
            self.faces['U'][i][2] = temp[i]
        self.move_history.append("R")

    def move_R_prime(self):
        self.rotate_face_counter_clockwise('R')
        temp = np.array([self.faces['F'][i][2] for i in range(3)])
        for i in range(3):
            self.faces['F'][i][2] = self.faces['U'][i][2]
            self.faces['U'][i][2] = self.faces['B'][2 - i][0]
            self.faces['B'][2 - i][0] = self.faces['D'][i][2]
            self.faces['D'][i][2] = temp[i]
        self.move_history.append("R'")

    def move_L(self):
        self.rotate_face_clockwise('L')
        temp = np.array([self.faces['F'][i][0] for i in range(3)])
        for i in range(3):
            self.faces['F'][i][0] = self.faces['U'][i][0]
            self.faces['U'][i][0] = self.faces['B'][2 - i][2]
            self.faces['B'][2 - i][2] = self.faces['D'][i][0]
            self.faces['D'][i][0] = temp[i]
        self.move_history.append("L")

    def move_L_prime(self):
        self.rotate_face_counter_clockwise('L')
        temp = np.array([self.faces['F'][i][0] for i in range(3)])
        for i in range(3):
            self.faces['F'][i][0] = self.faces['D'][i][0]
            self.faces['D'][i][0] = self.faces['B'][2 - i][2]
            self.faces['B'][2 - i][2] = self.faces['U'][i][0]
            self.faces['U'][i][0] = temp[i]
        self.move_history.append("L'")

    def move_F(self):
        self.rotate_face_clockwise('F')
        temp = self.faces['U'][2].copy()
        self.faces['U'][2] = np.array([self.faces['L'][2 - i][2] for i in range(3)])
        for i in range(3):
            self.faces['L'][i][2] = self.faces['D'][0][i]
        self.faces['D'][0] = np.array([self.faces['R'][2 - i][0] for i in range(3)])
        for i in range(3):
            self.faces['R'][i][0] = temp[i]
        self.move_history.append("F")

    def move_F_prime(self):
        self.rotate_face_counter_clockwise('F')
        temp = self.faces['U'][2].copy()
        self.faces['U'][2] = np.array([self.faces['R'][i][0] for i in range(3)])
        for i in range(3):
            self.faces['R'][i][0] = self.faces['D'][0][2 - i]
        self.faces['D'][0] = np.array([self.faces['L'][i][2] for i in range(3)])
        for i in range(3):
            self.faces['L'][i][2] = temp[2 - i]
        self.move_history.append("F'")

    def move_B(self):
        self.rotate_face_clockwise('B')
        temp = self.faces['U'][0].copy()
        self.faces['U'][0] = np.array([self.faces['R'][i][2] for i in range(3)])
        for i in range(3):
            self.faces['R'][i][2] = self.faces['D'][2][2 - i]
        self.faces['D'][2] = np.array([self.faces['L'][i][0] for i in range(3)])
        for i in range(3):
            self.faces['L'][i][0] = temp[2 - i]
        self.move_history.append("B")

    def move_B_prime(self):
        self.rotate_face_counter_clockwise('B')
        temp = self.faces['U'][0].copy()
        self.faces['U'][0] = np.array([self.faces['L'][2 - i][0] for i in range(3)])
        for i in range(3):
            self.faces['L'][i][0] = self.faces['D'][2][i]
        self.faces['D'][2] = np.array([self.faces['R'][2 - i][2] for i in range(3)])
        for i in range(3):
            self.faces['R'][i][2] = temp[i]
        self.move_history.append("B'")

    def execute_move(self, move):
        move = move.strip()
        if not move:
            return
        base = move[0]
        suffix = move[1:] if len(move) > 1 else ""

        def once(b):
            if b == 'U': self.move_U()
            elif b == 'D': self.move_D()
            elif b == 'R': self.move_R()
            elif b == 'L': self.move_L()
            elif b == 'F': self.move_F()
            elif b == 'B': self.move_B()

        if suffix == "2":
            once(base); once(base)
        elif suffix == "'":
            if base == 'U': self.move_U_prime()
            elif base == 'D': self.move_D_prime()
            elif base == 'R': self.move_R_prime()
            elif base == 'L': self.move_L_prime()
            elif base == 'F': self.move_F_prime()
            elif base == 'B': self.move_B_prime()
        else:
            once(base)

    def execute_algorithm(self, algorithm):
        for mv in algorithm.split():
            self.execute_move(mv)

    def scramble(self, moves):
        self.move_history = []
        self.last_scramble = moves.split()
        for mv in self.last_scramble:
            self.execute_move(mv)
        self.move_history = []

    def random_scramble(self, num_moves=20):
        basics = ["U", "D", "R", "L", "F", "B"]
        suffixes = ["", "'", "2"]
        seq = []
        prev_face = None
        for _ in range(num_moves):
            face = random.choice([b for b in basics if b != prev_face])
            prev_face = face
            mv = face + random.choice(suffixes)
            seq.append(mv)
        scramble_sequence = " ".join(seq)
        self.scramble(scramble_sequence)
        return scramble_sequence


class CubeSolver:
    def __init__(self, cube):
        self.cube = cube
        self.solution = []

    def get_solution(self):
        facelets = self.cube.to_kociemba_string()
        try:
            solution_str = kociemba.solve(facelets)
            self.solution = solution_str.split() if solution_str.strip() else []
        except Exception as e:
            print(f"Solver error: {e}")
            messagebox.showerror("Solver Error", f"Could not compute solution:\n{e}")
            self.solution = []
        return self.solution


class CubeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik's Cube Solver")
        self.root.geometry("1300x900")
        self.root.resizable(False, False)

        self.cube = RubiksCube()
        self.solving = False
        self.animation_speed = 500  # ms
        self.solution_moves = []
        self.solve_start_time = 0

        self.color_map = {
            'W': '#FFFFFF',
            'Y': '#FFFF00',
            'G': '#00FF00',
            'B': '#0000FF',
            'O': '#FFA500',
            'R': '#FF0000'
        }

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.cube_frame = ttk.Frame(self.main_frame)
        self.cube_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_frame = ttk.Frame(self.main_frame, width=300)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        self.canvas = tk.Canvas(self.cube_frame, width=1000, height=800, bg='lightgray')
        self.canvas.pack(pady=10)

        self.create_move_buttons()
        self.create_control_buttons()
        self.create_solution_display()

        self.draw_cube()

    def create_move_buttons(self):
        move_frame = ttk.LabelFrame(self.control_frame, text="Cube Moves", padding="10")
        move_frame.pack(fill=tk.X, pady=10)

        moves = [("U", "U'"), ("D", "D'"), ("R", "R'"), ("L", "L'"), ("F", "F'"), ("B", "B'")]
        for i, (m1, m2) in enumerate(moves):
            row = i // 2
            col = i % 2
            ttk.Button(move_frame, text=m1, width=5, command=lambda m=m1: self.make_move(m)) \
                .grid(row=row, column=col*2, padx=2, pady=2)
            ttk.Button(move_frame, text=m2, width=5, command=lambda m=m2: self.make_move(m)) \
                .grid(row=row, column=col*2+1, padx=2, pady=2)

        algo_row = (len(moves) - 1) // 2 + 1
        ttk.Label(move_frame, text="Run Algo:").grid(row=algo_row, column=0, padx=2, pady=4, sticky="w")
        self.algo_entry = ttk.Entry(move_frame, width=20)
        self.algo_entry.grid(row=algo_row, column=1, padx=2, pady=4, columnspan=2, sticky="we")
        ttk.Button(move_frame, text="Run", command=self.run_manual_algorithm) \
            .grid(row=algo_row, column=3, padx=2, pady=4)

    def create_control_buttons(self):
        control_frame = ttk.LabelFrame(self.control_frame, text="Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=10)

        self.scramble_btn = ttk.Button(control_frame, text="Scramble", command=self.scramble_cube)
        self.scramble_btn.pack(fill=tk.X, pady=2)

        self.solve_btn = ttk.Button(control_frame, text="Solve", command=self.start_solving)
        self.solve_btn.pack(fill=tk.X, pady=2)

        self.reset_btn = ttk.Button(control_frame, text="Reset", command=self.reset_cube)
        self.reset_btn.pack(fill=tk.X, pady=2)

        speed_frame = ttk.Frame(control_frame)
        speed_frame.pack(fill=tk.X, pady=5)
        ttk.Label(speed_frame, text="Animation Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.IntVar(value=500)
        speed_scale = ttk.Scale(
            speed_frame, from_=50, to=1000, variable=self.speed_var,
            orient=tk.HORIZONTAL, command=self.update_speed
        )
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def create_solution_display(self):
        solution_frame = ttk.LabelFrame(self.control_frame, text="Solution", padding="10")
        solution_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.solution_text = tk.Text(solution_frame, height=15, width=30, wrap=tk.WORD, state=tk.DISABLED)
        self.solution_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(solution_frame, command=self.solution_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.solution_text.config(yscrollcommand=scrollbar.set)

    def update_speed(self, value):
        self.animation_speed = int(float(value))

    def draw_cube(self):
        self.canvas.delete("all")
        face_size = 150
        cell_size = face_size // 3

        positions = {
            'U': (425, 50),
            'L': (100, 250),
            'F': (300, 250),
            'R': (500, 250),
            'B': (700, 250),
            'D': (425, 450)
        }

        for face, (x, y) in positions.items():
            self.canvas.create_rectangle(x, y, x + face_size, y + face_size, fill='black', outline='black', width=2)
            for i in range(3):
                for j in range(3):
                    cell_x = x + j * cell_size
                    cell_y = y + i * cell_size
                    color = self.color_map[self.cube.faces[face][i][j]]
                    self.canvas.create_rectangle(
                        cell_x, cell_y, cell_x + cell_size, cell_y + cell_size,
                        fill=color, outline='black', width=1
                    )
            self.canvas.create_text(x + face_size // 2, y - 10, text=face, font=('Arial', 12, 'bold'))

    def make_move(self, move):
        if not self.solving:
            self.cube.execute_move(move)
            self.draw_cube()

    def run_manual_algorithm(self):
        if self.solving:
            return
        algo = self.algo_entry.get().strip()
        if not algo:
            return
        self.cube.execute_algorithm(algo)
        self.draw_cube()

    def scramble_cube(self):
        if not self.solving:
            scramble_sequence = self.cube.random_scramble(20)
            self.draw_cube()
            self.solution_text.config(state=tk.NORMAL)
            self.solution_text.delete(1.0, tk.END)
            self.solution_text.insert(tk.END, f"Scramble: {scramble_sequence}\n")
            self.solution_text.config(state=tk.DISABLED)

    def reset_cube(self):
        if not self.solving:
            self.cube = RubiksCube()
            self.draw_cube()
            self.solution_text.config(state=tk.NORMAL)
            self.solution_text.delete(1.0, tk.END)
            self.solution_text.config(state=tk.DISABLED)

    def start_solving(self):
        if self.solving:
            return
        if self.cube.is_solved():
            messagebox.showinfo("Already Solved", "The cube is already solved.")
            return

        if not KOCIEMBA_AVAILABLE:
            messagebox.showerror(
                "Solver Unavailable",
                "The kociemba package is not installed. Install in the active venv: pip install kociemba"
            )
            return

        self.solver = CubeSolver(self.cube)
        self.solution_moves = self.solver.get_solution()

        if not self.solution_moves:
            messagebox.showwarning("No Solution", "Solver returned no moves (cube might already be solved or invalid).")
            return

        self.solving = True
        self.solve_btn.config(state=tk.DISABLED)
        self.scramble_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)

        self.solve_start_time = time.time()
        self.solution_text.config(state=tk.NORMAL)
        self.solution_text.delete(1.0, tk.END)
        self.solution_text.insert(tk.END, "Solution:\n")
        self.solution_text.config(state=tk.DISABLED)

        self.animate_solution(self.solution_moves.copy())

    def animate_solution(self, solution):
        if solution:
            move = solution.pop(0)
            self.cube.execute_move(move)
            self.draw_cube()

            self.solution_text.config(state=tk.NORMAL)
            self.solution_text.insert(tk.END, f"{move} ")
            self.solution_text.see(tk.END)
            self.solution_text.config(state=tk.DISABLED)

            self.root.after(self.animation_speed, lambda: self.animate_solution(solution))
        else:
            self.solving = False
            self.solve_btn.config(state=tk.NORMAL)
            self.scramble_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)

            solve_time = time.time() - self.solve_start_time
            if self.cube.is_solved():
                messagebox.showinfo(
                    "Solution Complete",
                    f"Cube solved successfully in {solve_time:.2f} seconds with {len(self.solution_moves)} moves!"
                )
            else:
                messagebox.showwarning(
                    "Not Solved",
                    "The sequence finished but the cube is not solved.\n"
                    "Please check the scramble/moves or try again."
                )


def main():
    root = tk.Tk()
    app = CubeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
