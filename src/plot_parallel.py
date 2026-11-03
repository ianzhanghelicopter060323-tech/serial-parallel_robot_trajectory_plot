# ======================================================
# 本代码角度值单位为rad 长度值单位为mm 
# ======================================================
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
import math
from pathlib import Path


PI = math.pi
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


# 定义绘图函数
def plot_trajec() -> None :
    # 规定两关节最多转0到180度
    #theta = np.linspace(0, PI, 1001)
    #phi = np.linspace(0, PI, 1001)
    
    # 用参数方程给出不同的theta和phi，不然就一直是一条直线
    t = np.linspace(0, 2*np.pi, 500)
    theta = np.deg2rad(90 + 60*np.sin(t))
    phi   = np.deg2rad(90 + 60*np.cos(t))

    # 设置m, n, l1, l2, l3
    m = 100
    n = 100

    l1 = 300
    l2 = 300
    l3 = 300

    # 求解x, y
    # s, a, h是参数
    s = np.sqrt((l3 - n*np.cos(phi) - m*np.cos(theta))**2 + (n*np.sin(phi) - m*np.sin(theta))**2)
    a = (l1**2 - l2**2 + s**2) / (2*s)
    h = np.sqrt(l1**2 - a**2)

    # 取sigma为+1
    x1 = m*np.cos(theta) + (a/s)*(l3 - n*np.cos(phi) - m*np.cos(theta)) - (h/s)*(n*np.sin(phi) - m*np.sin(theta))
    y1 = m*np.sin(theta) + (a/s)*(n*np.sin(phi) - m*np.sin(theta)) + (h/s)*(l3 - n*np.cos(phi) - m*np.cos(theta))
    # 取sigma为-1
    x2 = m*np.cos(theta) + (a/s)*(l3 - n*np.cos(phi) - m*np.cos(theta)) + (h/s)*(n*np.sin(phi) - m*np.sin(theta))
    y2 = m*np.sin(theta) + (a/s)*(n*np.sin(phi) - m*np.sin(theta)) - (h/s)*(l3 - n*np.cos(phi) - m*np.cos(theta))

    # 在同一组坐标轴中绘制两条轨迹
    fig, ax = plt.subplots(figsize=(7, 9))
    ax.plot(x1, y1, 'b', label="End-effector trajectory 1")
    ax.plot(x2, y2, 'y', label="End-effector trajectory 2")
    # 空心圆和叉号使闭合轨迹上重合的起终点仍可辨认
    ax.scatter([x1[0], x2[0]], [y1[0], y2[0]],
               facecolors="none", edgecolors="green", s=90,
               label="Start", zorder=3)
    ax.scatter([x1[-1], x2[-1]], [y1[-1], y2[-1]],
               color="red", marker=MarkerStyle("x"), s=40, label="End", zorder=4)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    # 根据两条轨迹的范围设置刻度，避免截断新的参数轨迹
    x_min = 25 * np.floor(min(x1.min(), x2.min()) / 25) - 25
    x_max = 25 * np.ceil(max(x1.max(), x2.max()) / 25) + 25
    ax.set_xlim(x_min, x_max)
    ax.set_xticks(np.arange(50 * np.ceil(x_min / 50), x_max + 1, 50))
    ax.set_title("2DOF parallel robot end effector trajectories")
    # 横纵坐标使用相同的比例，避免轨迹变形
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout()

    # 仅保存合并后的图片
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "trajectory_parallel.png"

    fig.savefig(str(output_path), dpi=300, bbox_inches="tight")
    print(f"并联轨迹图片已保存在:{output_path}")

    plt.show()


if __name__ == "__main__" :
    plot_trajec()

