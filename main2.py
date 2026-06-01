import tkinter as tk

root = tk.Tk()
root.title("Решение ОДУ")

# Поля ввода
tk.Label(root, text="f(t,u) =").grid(row=0, column=0)
entry_f = tk.Entry(root, width=25)
entry_f.insert(0, "u - t**2 + 1")
entry_f.grid(row=0, column=1)

tk.Label(root, text="t0 =").grid(row=1, column=0)
entry_t0 = tk.Entry(root, width=10)
entry_t0.insert(0, "0")
entry_t0.grid(row=1, column=1)

tk.Label(root, text="T =").grid(row=2, column=0)
entry_T = tk.Entry(root, width=10)
entry_T.insert(0, "2")
entry_T.grid(row=2, column=1)

tk.Label(root, text="u0 =").grid(row=3, column=0)
entry_u0 = tk.Entry(root, width=10)
entry_u0.insert(0, "0.5")
entry_u0.grid(row=3, column=1)

tk.Label(root, text="h =").grid(row=4, column=0)
entry_h = tk.Entry(root, width=10)
entry_h.insert(0, "0.1")
entry_h.grid(row=4, column=1)

# Кнопка (пока ничего не делает)
btn = tk.Button(root, text="Решить и построить")
btn.grid(row=5, column=0, columnspan=2)

canvas = tk.Canvas(root, width=600, height=400, bg='white')
canvas.grid(row=6, column=0, columnspan=2)

root.mainloop()