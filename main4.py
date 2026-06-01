import tkinter as tk
import math

root = tk.Tk()
root.title("Решение ОДУ (Эйлер и Хойн)")

# Поля ввода (аналогично предыдущему)
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

canvas = tk.Canvas(root, width=600, height=400, bg='white')
canvas.grid(row=6, column=0, columnspan=2)

status = tk.Label(root, text="Введите данные и нажмите кнопку", fg="blue")
status.grid(row=7, column=0, columnspan=2)

def solve():
    try:
        expr = entry_f.get()
        t0 = float(entry_t0.get())
        T = float(entry_T.get())
        u0 = float(entry_u0.get())
        h = float(entry_h.get())

        if t0 >= T or h <= 0:
            status.config(text="Ошибка в данных", fg="red")
            return

        allowed = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
            'pi': math.pi, 'e': math.e, 'abs': abs, 'pow': pow
        }
        def f(t, u):
            return eval(expr, {"__builtins__": {}}, {**allowed, 't': t, 'u': u})

        # Эйлер
        t_euler, u_euler = [t0], [u0]
        t, u = t0, u0
        while t < T - 1e-12:
            u = u + h * f(t, u)
            t = t + h
            t_euler.append(t); u_euler.append(u)

        # Хойн
        t_heun, u_heun = [t0], [u0]
        t, u = t0, u0
        while t < T - 1e-12:
            k1 = f(t, u)
            u_pred = u + h * k1
            k2 = f(t + h, u_pred)
            u = u + h * 0.5 * (k1 + k2)
            t = t + h
            t_heun.append(t); u_heun.append(u)

        # Графика
        canvas.delete("all")
        W, H = 600, 400
        margin = 50
        all_u = u_euler + u_heun
        u_min, u_max = min(all_u), max(all_u)
        if u_min == u_max:
            u_min -= 1; u_max += 1
        t_min, t_max = t0, T

        def tx(t_val):
            return margin + (t_val - t_min)/(t_max - t_min)*(W - 2*margin)
        def ty(u_val):
            return H - margin - (u_val - u_min)/(u_max - u_min)*(H - 2*margin)

        canvas.create_line(margin, H-margin, W-margin, H-margin, arrow=tk.LAST)
        canvas.create_line(margin, H-margin, margin, margin, arrow=tk.LAST)

        # Эйлер (синий)
        pts = []
        for i in range(len(t_euler)):
            pts.extend([tx(t_euler[i]), ty(u_euler[i])])
        canvas.create_line(pts, fill="blue", width=2)
        # Легенда Эйлер
        canvas.create_line(W-150, 20, W-130, 20, fill="blue", width=2)
        canvas.create_text(W-120, 20, text="Эйлер", anchor=tk.W)

        # Хойн (красный)
        pts = []
        for i in range(len(t_heun)):
            pts.extend([tx(t_heun[i]), ty(u_heun[i])])
        canvas.create_line(pts, fill="red", width=2)
        # Легенда Хойн
        canvas.create_line(W-150, 40, W-130, 40, fill="red", width=2)
        canvas.create_text(W-120, 40, text="Хойн", anchor=tk.W)

        status.config(text="График построен", fg="green")

    except Exception as e:
        status.config(text=f"Ошибка: {e}", fg="red")

btn = tk.Button(root, text="Решить и построить", command=solve)
btn.grid(row=5, column=0, columnspan=2)

root.mainloop()