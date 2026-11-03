import math
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


PI = math.pi


# 定义绘图函数
def plot_trajec() -> None :
    # 规定两关节最多转-90到90
    theta_1 = np.linspace(-PI/2, PI/2, 1001)
    theta_2 = np.linspace(-PI/2, PI/2, 1001)
    
    # 给定l1, l2取值
    l1 = 10
    l2 = 5

    x = l1 * np.cos(theta_1) + l2 * np.cos(theta_1 + theta_2)
    y = l1 * np.sin(theta_1) + l2 * np.sin(theta_1 + theta_2)

    # 绘图
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(x, y, label="End-effector trajectory")
    ax.scatter(x[0], y[0], color="green", label="Start", zorder=3)
    ax.scatter(x[-1], y[-1], color="red", label="End", zorder=3)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Two-link arm trajectory")

    # 横纵坐标使用相同的比例，避免轨迹变形
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()

    # 按脚本位置确定输出目录，不受运行时工作目录影响
    output_dir = Path(__file__).resolve().parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "trajectory_serial.png"
    fig.savefig(str(output_path), dpi=300, bbox_inches="tight")
    print(f"图片已保存至：{output_path}")
    plt.show()


if __name__ == "__main__":
    plot_trajec()


