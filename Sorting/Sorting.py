import tkinter as tk
from tkinter import ttk
import random
import threading
import time


class SortingVisualizer(tk.Tk):
    def _init_(self):
        super()._init_()

        self.title("Sorting Visualizer")
        self.geometry("800x600")
        self.configure(bg='#F0F0F0')

        self.array = self.generate_random_array(50)
        self.delay = 50
        self.current_swap1 = -1
        self.current_swap2 = -1

        self.create_widgets()

    def create_widgets(self):
        self.heading_label = tk.Label(self, text="Sorting Visualizer", font=("Serif", 28, "bold"), bg='#C8C8FF')
        self.heading_label.pack(pady=10)

        self.control_frame = tk.Frame(self, bg='#C8C8FF')
        self.control_frame.pack(pady=10)

        self.algorithm_label = tk.Label(self.control_frame, text="Algorithm:", bg='#C8C8FF')
        self.algorithm_label.grid(row=0, column=0, padx=5)

        self.algorithm_input = ttk.Entry(self.control_frame, width=10)
        self.algorithm_input.grid(row=0, column=1, padx=5)

        self.start_button = ttk.Button(self.control_frame, text="Start Sorting", command=self.start_sorting)
        self.start_button.grid(row=0, column=2, padx=5)

        self.speed_label = tk.Label(self.control_frame, text="Speed:", bg='#C8C8FF')
        self.speed_label.grid(row=0, column=3, padx=5)

        self.speed_slider = ttk.Scale(self.control_frame, from_=0, to_=1000, orient="horizontal",
                                      command=self.update_delay)
        self.speed_slider.set(self.delay)
        self.speed_slider.grid(row=0, column=4, padx=5)

        self.size_label = tk.Label(self.control_frame, text="Number of Bars:", bg='#C8C8FF')
        self.size_label.grid(row=0, column=5, padx=5)

        self.size_slider = ttk.Scale(self.control_frame, from_=10, to_=100, orient="horizontal",
                                     command=self.update_array_size)
        self.size_slider.set(len(self.array))
        self.size_slider.grid(row=0, column=6, padx=5)

        self.description_area = tk.Text(self, height=5, width=50, wrap="word", bg='#C8C8FF', state="disabled")
        self.description_area.pack(pady=10)

        self.canvas = tk.Canvas(self, width=800, height=400, bg='#F0F0F0')
        self.canvas.pack()

        self.update_canvas()

    def generate_random_array(self, size):
        array = [random.randint(1, size) for _ in range(size)]
        return array

    def update_delay(self, value):
        self.delay = int(float(value))

    def update_array_size(self, value):
        size = int(float(value))
        self.array = self.generate_random_array(size)
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        width = 800
        height = 400
        bar_width = width / len(self.array)

        for i in range(len(self.array)):
            x0 = i * bar_width
            y0 = height - (self.array[i] / max(self.array)) * height
            x1 = (i + 1) * bar_width
            y1 = height

            color = "red" if i == self.current_swap1 or i == self.current_swap2 else f'#{100 + (self.array[i] * 155 // len(self.array)):02x}{100 + (self.array[i] * 155 // len(self.array)):02x}{100 + (self.array[i] * 155 // len(self.array)):02x}'
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            self.canvas.create_text(x0 + bar_width / 2, y0, text=str(self.array[i]), anchor="s", fill="white")

    def swap(self, i, j):
        self.array[i], self.array[j] = self.array[j], self.array[i]
        self.current_swap1, self.current_swap2 = i, j
        self.update_canvas()
        self.update()
        time.sleep(self.delay / 1000)
        self.current_swap1, self.current_swap2 = -1, -1
        self.update_canvas()
        self.update()
        time.sleep(self.delay / 1000)

    def bubble_sort(self):
        for i in range(len(self.array) - 1):
            for j in range(len(self.array) - i - 1):
                if self.array[j] > self.array[j + 1]:
                    self.swap(j, j + 1)

    def insertion_sort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i - 1
            while j >= 0 and self.array[j] > key:
                self.array[j + 1] = self.array[j]
                j -= 1
                self.update_canvas()
                self.update()
                time.sleep(self.delay / 1000)
            self.array[j + 1] = key
            self.update_canvas()
            self.update()
            time.sleep(self.delay / 1000)

    def selection_sort(self):
        for i in range(len(self.array) - 1):
            min_idx = i
            for j in range(i + 1, len(self.array)):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            self.swap(i, min_idx)

    def merge_sort(self):
        self.merge_sort_helper(0, len(self.array) - 1)

    def merge_sort_helper(self, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort_helper(left, mid)
            self.merge_sort_helper(mid + 1, right)
            self.merge(left, mid, right)

    def merge(self, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid

        L = self.array[left:mid + 1]
        R = self.array[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                self.array[k] = L[i]
                i += 1
            else:
                self.array[k] = R[j]
                j += 1
            k += 1
            self.update_canvas()
            self.update()
            time.sleep(self.delay / 1000)

        while i < n1:
            self.array[k] = L[i]
            i += 1
            k += 1
            self.update_canvas()
            self.update()
            time.sleep(self.delay / 1000)

        while j < n2:
            self.array[k] = R[j]
            j += 1
            k += 1
            self.update_canvas()
            self.update()
            time.sleep(self.delay / 1000)

    def quick_sort(self):
        self.quick_sort_helper(0, len(self.array) - 1)

    def quick_sort_helper(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort_helper(low, pi - 1)
            self.quick_sort_helper(pi + 1, high)

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1

        for j in range(low, high):
            if self.array[j] <= pivot:
                i += 1
                self.swap(i, j)
        self.swap(i + 1, high)
        return i + 1

    def start_sorting(self):
        algorithm = self.algorithm_input.get().lower()
        self.description_area.config(state="normal")
        self.description_area.delete(1.0, tk.END)
        self.description_area.insert(tk.END, self.get_algorithm_description(algorithm))
        self.description_area.config(state="disabled")

        threading.Thread(target=self.run_sorting_algorithm, args=(algorithm,)).start()

    def run_sorting_algorithm(self, algorithm):
        try:
            if algorithm == "bubble":
                self.bubble_sort()
            elif algorithm == "insertion":
                self.insertion_sort()
            elif algorithm == "selection":
                self.selection_sort()
            elif algorithm == "merge":
                self.merge_sort()
            elif algorithm == "quick":
                self.quick_sort()
            else:
                self.description_area.config(state="normal")
                self.description_area.delete(1.0, tk.END)
                self.description_area.insert(tk.END,
                                             "Unknown algorithm. Please enter: bubble, insertion, selection, merge, or quick.")
                self.description_area.config(state="disabled")
        except Exception as e:
            print(e)

    def get_algorithm_description(self, algorithm):
        descriptions = {
            "bubble": "Bubble Sort:\nAverage Time: O(n^2)\nWorst Time: O(n^2)\nBest Time: O(n)\nSpace: O(1)",
            "insertion": "Insertion Sort:\nAverage Time: O(n^2)\nWorst Time: O(n^2)\nBest Time: O(n)\nSpace: O(1)",
            "selection": "Selection Sort:\nAverage Time: O(n^2)\nWorst Time: O(n^2)\nBest Time: O(n^2)\nSpace: O(1)",
            "merge": "Merge Sort:\nAverage Time: O(n log n)\nWorst Time: O(n log n)\nBest Time: O(n log n)\nSpace: O(n)",
            "quick": "Quick Sort:\nAverage Time: O(n log n)\nWorst Time: O(n^2)\nBest Time: O(n log n)\nSpace: O(log n)"
        }
        return descriptions.get(algorithm,
                                "Unknown algorithm. Please enter: bubble, insertion, selection, merge, or quick.")


if __name__ == "_main_":
    app = SortingVisualizer()
    app.mainloop()