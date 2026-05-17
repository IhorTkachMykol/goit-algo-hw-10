import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.integrate as spi

# ── Функція та межі ────────────────────────────────────────────────────────────
def f(x):
    return x ** 2 + 1

a, b = 0, 2

# ── 1. Метод Монте-Карло ───────────────────────────────────────────────────────
np.random.seed(42)
N = 1_000_000

x_rand = np.random.uniform(a, b, N)
y_max  = f(b)
y_rand = np.random.uniform(0, y_max, N)

under  = y_rand <= f(x_rand)
monte_carlo_result = (b - a) * y_max * np.sum(under) / N

# ── 2. Аналітичне: ∫(x²+1)dx = x³/3 + x  на [0,2] = 8/3 + 2 = 14/3 ≈ 4.6̄ ──
analytical_result = (b**3 / 3 + b) - (a**3 / 3 + a)

# ── 3. scipy quad ─────────────────────────────────────────────────────────────
quad_result, quad_error = spi.quad(f, a, b)

# ── Виведення ─────────────────────────────────────────────────────────────────
print("=" * 52)
print(f"  Метод          │  Результат    │  Похибка")
print("─" * 52)
print(f"  Монте-Карло    │  {monte_carlo_result:.6f}   │  {abs(monte_carlo_result - analytical_result):.6f}")
print(f"  Аналітичний    │  {analytical_result:.6f}   │  0.000000")
print(f"  quad (SciPy)   │  {quad_result:.6f}   │  {quad_error:.2e}")
print("=" * 52)
print(f"\n  Відносна похибка МК: {abs(monte_carlo_result - analytical_result)/analytical_result*100:.4f}%")

# ── Графік ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor("#0f0f1a")
for ax in axes:
    ax.set_facecolor("#0f0f1a")

ACCENT = "#e8c14e"
RED    = "#ff6b6b"
BLUE   = "#4ecdc4"
GRID   = "#1e1e30"

ax1 = axes[0]
xs = np.linspace(-0.3, 2.3, 600)
ax1.plot(xs, f(xs), color=RED, linewidth=2.5, label=r"$f(x) = x^2 + 1$")
ix = np.linspace(a, b, 400)
ax1.fill_between(ix, f(ix), alpha=0.35, color=ACCENT,
                 label=f"Площа ≈ {monte_carlo_result:.4f}")
ax1.axvline(x=a, color="white", linestyle="--", linewidth=0.8, alpha=0.5)
ax1.axvline(x=b, color="white", linestyle="--", linewidth=0.8, alpha=0.5)
ax1.set_xlim(-0.3, 2.3)
ax1.set_ylim(0, f(b) + 0.5)
ax1.set_xlabel("x", color="white", fontsize=12)
ax1.set_ylabel("f(x)", color="white", fontsize=12)
ax1.set_title(r"Інтеграл $\int_0^2 (x^2+1)\,dx$", color="white", fontsize=13, pad=12)
ax1.tick_params(colors="white")
for spine in ax1.spines.values():
    spine.set_edgecolor(GRID)
ax1.grid(color=GRID, linewidth=0.8)
ax1.legend(facecolor="#1a1a2e", labelcolor="white", fontsize=10)

ax2 = axes[1]
SHOW = 6_000
idx  = np.random.choice(N, SHOW, replace=False)
ax2.scatter(x_rand[idx][~under[idx]], y_rand[idx][~under[idx]],
            s=0.8, color=RED, alpha=0.5)
ax2.scatter(x_rand[idx][under[idx]],  y_rand[idx][under[idx]],
            s=0.8, color=BLUE, alpha=0.5)
ax2.plot(np.linspace(a, b, 300), f(np.linspace(a, b, 300)),
         color=ACCENT, linewidth=2, zorder=5)
ax2.set_xlim(a, b)
ax2.set_ylim(0, y_max)
ax2.set_xlabel("x", color="white", fontsize=12)
ax2.set_ylabel("y", color="white", fontsize=12)
ax2.set_title(f"Метод Монте-Карло  (N = {N:,})", color="white", fontsize=13, pad=12)
ax2.tick_params(colors="white")
for spine in ax2.spines.values():
    spine.set_edgecolor(GRID)
ax2.grid(color=GRID, linewidth=0.8)
blue_patch = mpatches.Patch(color=BLUE, label=f"Під кривою: {np.sum(under):,}")
red_patch  = mpatches.Patch(color=RED,  label=f"Поза кривою: {N-np.sum(under):,}")
ax2.legend(handles=[blue_patch, red_patch],
           facecolor="#1a1a2e", labelcolor="white", fontsize=9)

plt.tight_layout(pad=2)
plt.savefig("monte_carlo.png", dpi=160,
            bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()