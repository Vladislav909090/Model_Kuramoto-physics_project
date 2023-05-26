import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# задаем радиус (пока не нужен)
R = 1
# общее время видео
t_all = 30
# шаг интегрирования
dt = 0.01
# время, через которое нужно получить следующую фазу
t = 0.05
# количество итераций, необходимых для достижения заданного времени
steps = int(t / dt)
# количество объектов на графике
N = 5

# создаем массив фаз и угловых скоростей каждого объекта
theta_points = np.random.uniform(0, np.pi, size=(N, 1))
omega_points = np.random.uniform(np.pi/4, np.pi, size=(N, 1))

# создаем массив связей между точками
K_mas = np.random.uniform(2, 3, size=(N, N))
K_mas = (K_mas + K_mas.T) / 2

# выводим значения для проверки
print("omega_points")
print(omega_points, end="\n\n")
print("theta_points")
print(theta_points, end="\n\n")
print("K_mas")
print(K_mas, end="\n\n")

# рассчитываем фазы для каждого момента времени
for _ in range(int(t_all/t)):
    # добавляем в массив theta_points и omega_points новый столбец с нулевыми элементами
    theta_points = np.pad(theta_points, [(0, 0), (0, 1)], constant_values=0)
    omega_points = np.pad(omega_points, [(0, 0), (0, 1)], constant_values=0)
    # рассчитываем фазы для каждого шага времени
    for i in range(steps):
        for j in range(N):
            theta_points[j][-1] = theta_points[j][-2] + \
                omega_points[j][0] * dt / 2
        for j in range(N):
            sum_sin = 0
            for k in range(N):
                if k == j:
                    continue
                else:
                    sum_sin += np.sin(theta_points[k]
                                      [-1]-theta_points[j][-1])*K_mas[k][j]
            theta_points[j][-1] += omega_points[j][0] * \
                dt / 2 + sum_sin * dt / N
            omega_points[j][-1] = (theta_points[j][-1] -
                                   theta_points[j][-2]) / dt

# выводим значения для проверки
print("theta_points")
print(theta_points.shape, end="\n\n")
print(theta_points, end="\n\n")
print("omega_points")
print(omega_points.shape, end="\n\n")
print(omega_points, end="\n\n")


# создаем график
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13, 4))
plt.suptitle(f'Модель Курамото, N={N}')

# mas_of_colors = np.random.uniform(0, 1, size=(N, 3))
mas_of_colors_min_max = np.empty((N, ))
for i in range(N):
    mas_of_colors_min_max[i] = (np.sum(K_mas[i]))

mas_of_colors = np.empty((N, 3))
for i in range(N):
    mas_of_colors[i] = [(np.sum(K_mas[i])-np.min(mas_of_colors_min_max)) /
                        (np.max(mas_of_colors_min_max)-np.min(mas_of_colors_min_max)), 0, 0]
    print(mas_of_colors[i])
time_intervals = np.arange(0, t_all, t)

ax1.set_xlim(-1.2, 1.2)  # Границы по оси x
ax1.set_ylim(-1.2, 1.2)  # Границы по оси y
ax1.set_aspect('equal')
ax1.set_title('Симуляция движения объектов')  # Заголовок для первого графика
# рисуем единичную окружность
mas_for_graph = np.linspace(0, 2*np.pi, 100)
ax1.plot(np.sin(mas_for_graph), np.cos(mas_for_graph), color='black', lw=0.8)
# создаем точки для каждого объекта
points = ax1.scatter([], [], s=50)


ax2.set_xlim(0, time_intervals[-1])  # Границы по оси x
ax2.set_ylim(-3, 3)  # Границы по оси y -3 3
ax2.set_title('theta(t)')  # Заголовок для первого графика
lines2 = []
for i in range(N):
    lines2.append(ax2.plot([], [], color=mas_of_colors[i])[0])


ax3.set_xlim(0, time_intervals[-1])  # Границы по оси x
ax3.set_ylim(np.min(omega_points)-0.5,
             np.max(omega_points)+0.5)  # Границы по оси y
ax3.set_title('omega(t)')  # Заголовок для первого графика
lines3 = []
for i in range(N):
    lines3.append(ax3.plot([], [], color=mas_of_colors[i])[0])

# функция для обновления графика на каждом шаге анимации


def update(frame):
    x = []
    y = []
    # рассчитываем координаты для каждой точки
    for i in range(N):
        x.append(np.cos(theta_points[i][frame]))
        y.append(np.sin(theta_points[i][frame]))
        lines2[i].set_xdata(time_intervals[:frame])
        lines2[i].set_ydata(np.sin(theta_points[i][:frame]))
        lines3[i].set_xdata(time_intervals[:frame])
        lines3[i].set_ydata(omega_points[i][:frame])
    points.set_offsets(np.column_stack([x, y]))
    points.set_color(mas_of_colors)


# создаем гифку на основе сформированных кадров
ani = animation.FuncAnimation(
    fig=fig, func=update, frames=int(t_all/t), interval=int(t*1000))
# показываем анимацию
plt.show()

# сохраняем анимацию в .gif
print("animation is generated")
ani.save(filename="Model Kuramoto.mp4", writer="pillow")
print("program finished")
