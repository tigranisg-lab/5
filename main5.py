import tkinter as tk
import math

root = tk.Tk()
root.title("Решение ОДУ (Эйлер и Хойн)")

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

btn = tk.Button(root, text="Решить и построить")
btn.grid(row=5, column=0, columnspan=2)

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

        if t0 >= T:
            status.config(text="Ошибка: t0 должно быть меньше T", fg="red")
            return
        if h <= 0:
            status.config(text="Ошибка: шаг h должен быть > 0", fg="red")
            return

        allowed = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'exp': math.exp, 'log': math.log, 'log10': math.log10,
            'sqrt': math.sqrt, 'pi': math.pi, 'e': math.e,
            'abs': abs, 'pow': pow
        }

        def f(t, u):
            return eval(expr, {"__builtins__": {}}, {**allowed, 't': t, 'u': u})

        try:
            f(0, 0)
        except Exception as e:
            status.config(text=f"Ошибка в формуле: {e}", fg="red")
            return

        # Метод Эйлера
        t_euler = [t0]
        u_euler = [u0]
        t = t0
        u = u0
        while t < T - 1e-12:
            u = u + h * f(t, u)
            t = t + h
            t_euler.append(t)
            u_euler.append(u)

        # Метод Хойна
        t_heun = [t0]
        u_heun = [u0]
        t = t0
        u = u0
        while t < T - 1e-12:
            k1 = f(t, u)
            u_pred = u + h * k1
            k2 = f(t + h, u_pred)
            u = u + h * 0.5 * (k1 + k2)
            t = t + h
            t_heun.append(t)
            u_heun.append(u)

        # Рисование
        canvas.delete("all")
        W = 600
        H = 400
        margin = 50

        all_u = u_euler + u_heun
        u_min = min(all_u)
        u_max = max(all_u)
        if u_min == u_max:
            u_min -= 1
            u_max += 1
        t_min = t0
        t_max = T

        def tx(t_val):
            return margin + (t_val - t_min) / (t_max - t_min) * (W - 2 * margin)

        def ty(u_val):
            return H - margin - (u_val - u_min) / (u_max - u_min) * (H - 2 * margin)

        # Оси
        canvas.create_line(margin, H - margin, W - margin, H - margin, arrow=tk.LAST)
        canvas.create_line(margin, H - margin, margin, margin, arrow=tk.LAST)
        canvas.create_text(W - margin + 10, H - margin, text="t")
        canvas.create_text(margin - 10, margin, text="u")

        # Деления на оси t (5 интервалов)
        for i in range(6):
            val = t_min + i * (t_max - t_min) / 5
            x = tx(val)
            canvas.create_line(x, H - margin - 5, x, H - margin + 5)
            canvas.create_text(x, H - margin + 15, text=f"{val:.2f}")

        # Деления на оси u (5 интервалов)
        for i in range(6):
            val = u_min + i * (u_max - u_min) / 5
            y = ty(val)
            canvas.create_line(margin - 5, y, margin + 5, y)
            canvas.create_text(margin - 20, y, text=f"{val:.2f}")

        # Эйлер (синий)
        points = []
        for i in range(len(t_euler)):
            x = tx(t_euler[i])
            y = ty(u_euler[i])
            points.append(x)
            points.append(y)
        canvas.create_line(points, fill="blue", width=2)

        # Легенда для Эйлера (y = 20)
        canvas.create_line(W - 150, 20, W - 130, 20, fill="blue", width=2)
        canvas.create_text(W - 120, 20, text="Эйлер", anchor=tk.W)

        # Хойн (красный)
        points = []
        for i in range(len(t_heun)):
            x = tx(t_heun[i])
            y = ty(u_heun[i])
            points.append(x)
            points.append(y)
        canvas.create_line(points, fill="red", width=2)

        # Легенда для Хойна (y = 40)
        canvas.create_line(W - 150, 40, W - 130, 40, fill="red", width=2)
        canvas.create_text(W - 120, 40, text="Хойн", anchor=tk.W)

        status.config(text="График построен", fg="green")

    except ValueError as e:
        status.config(text=f"Ошибка в числах: {e}", fg="red")
    except Exception as e:
        status.config(text=f"Неизвестная ошибка: {e}", fg="red")

btn.config(command=solve)

root.mainloop()