import tkinter as tk
import time

class FPSCounter:
    def __init__(self, parent):
        self.parent = parent
        self.label_fps = tk.Label(parent, text="FPS: 0", font=("Arial", 24))
        self.label_fps.pack(pady=80)
        self.desired_fps = tk.IntVar()
        self.desired_fps.set(100)
        self.entry_fps = tk.Entry(parent, textvariable=self.desired_fps, font=("Arial", 18))
        self.entry_fps.pack(pady=80)
        self.start_time = time.time()
        self.frame_count = 0
        self.update_fps()

    def update_fps(self):
        current_time = time.time()
        self.frame_count += 1
        desired_fps = self.desired_fps.get()

        if desired_fps <= 0:
            self.label_fps.config(text="FPS: Error")
        elif desired_fps > 1000:  # Limit the maximum desired FPS
            self.label_fps.config(text="FPS: Too high")
        else:
            if current_time - self.start_time >= 1:
                fps = self.frame_count / (current_time - self.start_time)
                self.label_fps.config(text=f"FPS: {fps:.2f}")
                self.frame_count = 0
                self.start_time = current_time
            self.parent.after(1000 // desired_fps, self.update_fps)


def main():
    root = tk.Tk()
    root.title("FPS Counter")
    root.geometry("1920x1080")

    FPSCounter(root)

    root.mainloop()

if __name__ == "__main__":
    main()
