# -*- coding: utf-8 -*-
"""
COMBINED COMPARISON — NN vs Clarke-Wright
==========================================
Scribe Q5: Outputs & Interpretation
  - Side-by-side route maps
  - Bar chart: total distance, avg route length, num routes
  - Overlaid PDF and CDF distributions (100 runs)
  - Summary statistics table
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import norm

# ── Shared helpers ───────────────────────────────────────────
def euclidean(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def build_D(nodes):
    n = len(nodes)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i, j] = euclidean(nodes[i], nodes[j])
    return D

# ── Model 1: Nearest Neighbour ───────────────────────────────
def nearest_neighbour(stops, school):
    unvisited = stops.tolist()
    route     = [school.tolist()]
    current   = school.copy()
    while unvisited:
        nearest = min(unvisited,
                      key=lambda x: euclidean(current, np.array(x)))
        route.append(nearest)
        current = np.array(nearest)
        unvisited.remove(nearest)
    route.append(school.tolist())
    route = np.array(route)
    dist  = sum(euclidean(route[i], route[i+1]) for i in range(len(route)-1))
    return route, dist

# ── Model 2: Clarke-Wright ───────────────────────────────────
def compute_savings(D, n_stops):
    savings = []
    for i in range(1, n_stops + 1):
        for j in range(1, n_stops + 1):
            if i != j:
                s = D[i, 0] + D[0, j] - D[i, j]
                savings.append((s, i, j))
    savings.sort(key=lambda x: x[0], reverse=True)
    return savings

def clarke_wright(D, n_stops):
    routes   = [[0, k, 0] for k in range(1, n_stops + 1)]
    route_of = {k: k-1 for k in range(1, n_stops + 1)}

    for s_val, i, j in compute_savings(D, n_stops):
        ri_idx = route_of.get(i)
        rj_idx = route_of.get(j)
        if ri_idx is None or rj_idx is None:
            continue
        if ri_idx == rj_idx:
            continue
        ri, rj = routes[ri_idx], routes[rj_idx]
        if ri[-2] == i and rj[1] == j:
            merged = ri[:-1] + rj[1:]
            routes[ri_idx] = merged
            routes[rj_idx] = None
            for node in merged:
                if node != 0:
                    route_of[node] = ri_idx

    active = [r for r in routes if r is not None]
    nodes_arr = None  # resolved externally
    dist = 0
    return active, dist   # dist computed separately below

def cw_total_dist(routes, D):
    total = 0
    for r in routes:
        total += sum(D[r[t], r[t+1]] for t in range(len(r)-1))
    return total


# ════════════════════════════════════════════════════════════
# SINGLE-INSTANCE RUN (seed=42, same as uploaded codes)
# ════════════════════════════════════════════════════════════
np.random.seed(42)
num_stops  = 10
grid_size  = 100
stops      = np.random.randint(0, grid_size, (num_stops, 2)).astype(float)
school     = np.array([50.0, 50.0])
nodes      = np.vstack([school, stops])
D          = build_D(nodes)

nn_route, nn_dist       = nearest_neighbour(stops, school)
cw_routes_raw, _        = clarke_wright(D, num_stops)
cw_dist                 = cw_total_dist(cw_routes_raw, D)
cw_num_routes           = len(cw_routes_raw)

print("=" * 60)
print("  COMBINED COMPARISON — Nearest Neighbour vs Clarke-Wright")
print("=" * 60)
print(f"\n  NN  Total Distance  : {nn_dist:.4f}  |  Routes: 1")
print(f"  CW  Total Distance  : {cw_dist:.4f}  |  Routes: {cw_num_routes}")
improvement = (nn_dist - cw_dist) / nn_dist * 100
print(f"  CW improvement over NN : {improvement:.1f}%")


# ════════════════════════════════════════════════════════════
# FIGURE 1 — Side-by-side route maps
# ════════════════════════════════════════════════════════════
colours = plt.cm.tab10.colors
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# — NN map —
ax1.scatter(stops[:, 0], stops[:, 1], s=80, color='steelblue',
            zorder=3, label="Bus Stops")
ax1.scatter(school[0], school[1], marker='s', s=130, color='red',
            zorder=4, label="School (Depot)")
ax1.plot(nn_route[:, 0], nn_route[:, 1], '--', color='steelblue',
         linewidth=1.5, label=f"Route (d={nn_dist:.1f})")
for i, (x, y) in enumerate(stops):
    ax1.text(x + 1, y + 1, f"S{i}", fontsize=8)
ax1.set_title(f"Nearest Neighbour Route\nTotal Distance = {nn_dist:.2f}",
              fontsize=12)
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.legend(fontsize=8)

# — CW map —
ax2.scatter(stops[:, 0], stops[:, 1], s=80, color='steelblue',
            zorder=3, label="Bus Stops")
ax2.scatter(school[0], school[1], marker='s', s=130, color='red',
            zorder=4, label="School (Depot)")
for r_idx, route in enumerate(cw_routes_raw):
    coords = nodes[route]
    rd     = sum(D[route[t], route[t+1]] for t in range(len(route)-1))
    ax2.plot(coords[:, 0], coords[:, 1], '--',
             color=colours[r_idx % len(colours)],
             linewidth=1.5, label=f"Route {r_idx+1} (d={rd:.1f})")
for i, (x, y) in enumerate(stops):
    ax2.text(x + 1, y + 1, f"S{i}", fontsize=8)
ax2.set_title(f"Clarke-Wright Routes\nTotal Distance = {cw_dist:.2f}  "
              f"|  {cw_num_routes} route(s)", fontsize=12)
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.legend(fontsize=8)

plt.suptitle("Route Comparison — Nearest Neighbour vs Clarke-Wright (seed=42)",
             fontsize=13)
plt.tight_layout()
fig1.savefig("/mnt/user-data/outputs/comparison_route_maps.png", dpi=150,
             bbox_inches="tight")
print("\n  [Saved] comparison_route_maps.png")


# ════════════════════════════════════════════════════════════
# FIGURE 2 — Bar chart: key metrics side-by-side  (Scribe Q5)
# ════════════════════════════════════════════════════════════
metrics  = ["Total Distance", "Avg Route Length", "Num Routes"]
nn_vals  = [nn_dist,  nn_dist / 1,          1]
cw_vals  = [cw_dist,  cw_dist / cw_num_routes, cw_num_routes]

x     = np.arange(len(metrics))
width = 0.35

fig2, ax = plt.subplots(figsize=(9, 5))
b1 = ax.bar(x - width/2, nn_vals, width, label="Nearest Neighbour",
            color='steelblue', alpha=0.85)
b2 = ax.bar(x + width/2, cw_vals, width, label="Clarke-Wright",
            color='darkorange', alpha=0.85)

for bar in b1:
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 2, f"{bar.get_height():.1f}",
            ha='center', va='bottom', fontsize=9)
for bar in b2:
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 2, f"{bar.get_height():.1f}",
            ha='center', va='bottom', fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_ylabel("Value")
ax.set_title("Performance Metrics: NN vs Clarke-Wright (seed=42)",
             fontsize=12)
ax.legend()
plt.tight_layout()
fig2.savefig("/mnt/user-data/outputs/comparison_metrics_bar.png", dpi=150,
             bbox_inches="tight")
print("  [Saved] comparison_metrics_bar.png")


# ════════════════════════════════════════════════════════════
# FIGURE 3 — Overlaid PDF + CDF over 100 runs  (Scribe Q5)
# ════════════════════════════════════════════════════════════
print("\n  Running 100-seed analysis …")
nn_dists, cw_dists_list = [], []

for seed in range(100):
    np.random.seed(seed)
    s  = np.random.randint(0, grid_size, (num_stops, 2)).astype(float)
    sc = np.array([50.0, 50.0])

    # NN
    _, d_nn = nearest_neighbour(s, sc)
    nn_dists.append(d_nn)

    # CW
    nd   = np.vstack([sc, s])
    Ds   = build_D(nd)
    rts, _ = clarke_wright(Ds, num_stops)
    d_cw   = cw_total_dist(rts, Ds)
    cw_dists_list.append(d_cw)

nn_dists  = np.array(nn_dists)
cw_dists2 = np.array(cw_dists_list)

mu_nn, s_nn = nn_dists.mean(),  nn_dists.std()
mu_cw, s_cw = cw_dists2.mean(), cw_dists2.std()

# Summary statistics  (Scribe Q5)
print(f"\n  ── Summary Statistics (100 seeds) ──")
print(f"  {'Metric':<22}  {'NN':>10}  {'CW':>10}")
print(f"  {'-'*44}")
print(f"  {'Mean':<22}  {mu_nn:>10.2f}  {mu_cw:>10.2f}")
print(f"  {'Std Dev':<22}  {s_nn:>10.2f}  {s_cw:>10.2f}")
print(f"  {'Variance':<22}  {nn_dists.var():>10.2f}  {cw_dists2.var():>10.2f}")
print(f"  {'Min':<22}  {nn_dists.min():>10.2f}  {cw_dists2.min():>10.2f}")
print(f"  {'Max':<22}  {nn_dists.max():>10.2f}  {cw_dists2.max():>10.2f}")

x_nn = np.linspace(mu_nn - 4*s_nn, mu_nn + 4*s_nn, 300)
x_cw = np.linspace(mu_cw - 4*s_cw, mu_cw + 4*s_cw, 300)

fig3, axes = plt.subplots(1, 2, figsize=(14, 5))

# ── PDF ──────────────────────────────────────────────────────
axes[0].hist(nn_dists, bins=20, density=True, alpha=0.45,
             color='steelblue', edgecolor='white', label="NN Simulation")
axes[0].hist(cw_dists2, bins=20, density=True, alpha=0.45,
             color='darkorange', edgecolor='white', label="CW Simulation")
axes[0].plot(x_nn, norm.pdf(x_nn, mu_nn, s_nn),
             color='navy', linewidth=2,
             label=f"NN fit  μ={mu_nn:.1f}")
axes[0].plot(x_cw, norm.pdf(x_cw, mu_cw, s_cw),
             color='saddlebrown', linewidth=2, linestyle='--',
             label=f"CW fit  μ={mu_cw:.1f}")
axes[0].set_title("PDF — Total Distance Distribution\nNN vs Clarke-Wright (100 runs)",
                  fontsize=12)
axes[0].set_xlabel("Total Distance")
axes[0].set_ylabel("Density")
axes[0].legend(fontsize=9)

# ── CDF ──────────────────────────────────────────────────────
snn = np.sort(nn_dists)
scw = np.sort(cw_dists2)
cdf_nn = np.arange(1, len(snn)+1) / len(snn)
cdf_cw = np.arange(1, len(scw)+1) / len(scw)

axes[1].step(snn, cdf_nn, color='steelblue', linewidth=2,
             label="NN Empirical CDF")
axes[1].step(scw, cdf_cw, color='darkorange', linewidth=2,
             label="CW Empirical CDF")
axes[1].plot(x_nn, norm.cdf(x_nn, mu_nn, s_nn),
             color='navy', linestyle='--', linewidth=1.5)
axes[1].plot(x_cw, norm.cdf(x_cw, mu_cw, s_cw),
             color='saddlebrown', linestyle=':', linewidth=1.5)
axes[1].set_title("CDF — Total Distance Distribution\nNN vs Clarke-Wright (100 runs)",
                  fontsize=12)
axes[1].set_xlabel("Total Distance")
axes[1].set_ylabel("Cumulative Probability")
axes[1].legend(fontsize=9)

plt.suptitle("Statistical Analysis: NN vs Clarke-Wright — Distance Distributions",
             fontsize=13, y=1.02)
plt.tight_layout()
fig3.savefig("/mnt/user-data/outputs/comparison_pdf_cdf.png", dpi=150,
             bbox_inches="tight")
print("  [Saved] comparison_pdf_cdf.png")

print("\n" + "=" * 60)
print("  COMBINED COMPARISON COMPLETE")
print("=" * 60)
