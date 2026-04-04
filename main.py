import re
import difflib
import networkx as nx
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
matplotlib.rcParams["toolbar"] = "None"

from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# =========================
# GRAPH
# =========================
G = nx.Graph()

# =========================
# DATA
# =========================
mrt_data = [
    # NSL
    ["Woodlands", "Yishun", 7.3, 4.5, "#D42E12", "North-South Line"],
    ["Yishun", "Ang Mo Kio", 7.7, 4.8, "#D42E12", "North-South Line"],
    ["Ang Mo Kio", "Bishan", 2.4, 1.5, "#D42E12", "North-South Line"],
    ["Bishan", "Newton", 4.7, 2.9, "#D42E12", "North-South Line"],
    ["Newton", "Orchard", 1.2, 0.75, "#D42E12", "North-South Line"],
    ["Orchard", "Dhoby Ghaut", 1.8, 1.1, "#D42E12", "North-South Line"],

    # EWL
    ["Jurong East", "Clementi", 3.5, 2.2, "#009645", "East-West Line"],
    ["Clementi", "Buona Vista", 3.1, 1.9, "#009645", "East-West Line"],
    ["Buona Vista", "City Hall", 9.5, 5.9, "#009645", "East-West Line"],
    ["City Hall", "Bugis", 1.0, 0.6, "#009645", "East-West Line"],
    ["Bugis", "Paya Lebar", 4.8, 3.0, "#009645", "East-West Line"],

    # CCL
    ["HarbourFront", "Buona Vista", 8.0, 5.0, "#FA9E0D", "Circle Line"],
    ["Buona Vista", "Botanic Gardens", 3.4, 2.1, "#FA9E0D", "Circle Line"],
    ["Botanic Gardens", "Bishan", 6.6, 4.1, "#FA9E0D", "Circle Line"],
    ["Bishan", "Serangoon", 2.6, 1.6, "#FA9E0D", "Circle Line"],
    ["Serangoon", "Promenade", 7.9, 4.9, "#FA9E0D", "Circle Line"],

    # DTL
    ["Bukit Panjang", "Beauty World", 4.7, 2.9, "#005EC4", "Downtown Line"],
    ["Beauty World", "King Albert Park", 1.2, 0.75, "#005EC4", "Downtown Line"],
    ["King Albert Park", "Botanic Gardens", 4.0, 2.5, "#005EC4", "Downtown Line"],
    ["Botanic Gardens", "Newton", 2.7, 1.7, "#005EC4", "Downtown Line"],
    ["Newton", "Little India", 1.4, 0.9, "#005EC4", "Downtown Line"],
    ["Little India", "Bugis", 1.3, 0.8, "#005EC4", "Downtown Line"],

    # NEL
    ["HarbourFront", "Outram Park", 2.6, 1.6, "#9900AA", "North-East Line"],
    ["Outram Park", "Chinatown", 0.7, 0.4, "#9900AA", "North-East Line"],
    ["Chinatown", "Dhoby Ghaut", 2.0, 1.2, "#9900AA", "North-East Line"],
    ["Dhoby Ghaut", "Little India", 1.0, 0.6, "#9900AA", "North-East Line"],
    ["Little India", "Serangoon", 5.7, 3.5, "#9900AA", "North-East Line"],
    ["Serangoon", "Hougang", 3.3, 2.0, "#9900AA", "North-East Line"],
]

for s, t, km, mi, c, l in mrt_data:
    G.add_edge(s, t, km=km, miles=mi, color=c, line=l)

# =========================
# FARE
# =========================
def calculate_fare(distance):
    fare_table = [
        (3.2, 1.19),
        (4.2, 1.29),
        (5.2, 1.40),
        (6.2, 1.50),
        (7.2, 1.59),
        (8.2, 1.66),
        (9.2, 1.73),
        (10.2, 1.77),
        (11.2, 1.81),
        (12.2, 1.85),
        (13.2, 1.89),
        (14.2, 1.93),
        (15.2, 1.98),
        (16.2, 2.02),
        (17.2, 2.06),
        (18.2, 2.10),
        (19.2, 2.14),
    ]

    for max_dist, fare in fare_table:
        if distance <= max_dist:
            return fare

    extra = distance - 19.2
    return 2.14 + (extra * 0.04)


# =========================
# LAYOUT
# =========================
scale = 2.7

pos = {
    "Jurong East": (-10 * scale, 0),
    "Clementi": (-6.5 * scale, 0),
    "Buona Vista": (-4 * scale, 0),
    "City Hall": (0, 0),
    "Bugis": (4 * scale, 0),
    "Paya Lebar": (8 * scale, 0),

    "Woodlands": (0, 9 * scale),
    "Yishun": (0, 7 * scale),
    "Ang Mo Kio": (0, 6 * scale),
    "Bishan": (0, 5 * scale),
    "Newton": (0, 3.8 * scale),
    "Orchard": (0, 2.8 * scale),
    "Dhoby Ghaut": (0, 1.8 * scale),

    "Little India": (2.5 * scale, 3.2 * scale),

    "HarbourFront": (-5 * scale, -4 * scale),
    "Botanic Gardens": (-2 * scale, 4 * scale),
    "Serangoon": (5 * scale, 5 * scale),
    "Promenade": (5 * scale, -1 * scale),
    "Outram Park": (-2 * scale, -1 * scale),
    "Chinatown": (-1 * scale, 0.5 * scale),
    "Hougang": (7 * scale, 6 * scale),
    "Bukit Panjang": (-9 * scale, 7 * scale),
    "Beauty World": (-7 * scale, 6 * scale),
    "King Albert Park": (-5 * scale, 5 * scale),
}

text_pos = {
    "Woodlands": (1.15, 0.35),
    "Yishun": (1.10, 0.05),
    "Ang Mo Kio": (1.10, -0.05),
    "Bishan": (-2.55, 0.58),
    "Newton": (1.25, 0.2),
    "Orchard": (1.15, 0.1),
    "Dhoby Ghaut": (1.2, -0.1),

    "Jurong East": (-1.4, -0.95),
    "Clementi": (-1.15, -0.95),
    "Buona Vista": (0.25, -1.15),
    "City Hall": (-1.10, -1.10),
    "Bugis": (-0.65, -1.10),
    "Paya Lebar": (-1.4, -1),

    "Bukit Panjang": (-4, -1),
    "Beauty World": (-4.2, -0.6),
    "King Albert Park": (-5.05, -0.78),

    "Botanic Gardens": (-5.35, -0.2),
    "Little India": (1.4, 0),
    "Serangoon": (1.35, -0.1),
    "Promenade": (0.90, -0.92),
    "Hougang": (0.90, 0.20),

    "HarbourFront": (-2, -1.35),
    "Outram Park": (0.9, -0.15),
    "Chinatown": (0.9, 0.04),
}

edge_label_pos = {
    ("Woodlands", "Yishun"): (-0.45, 0.00),
    ("Yishun", "Ang Mo Kio"): (-0.45, 0.00),
    ("Ang Mo Kio", "Bishan"): (-0.48, 0.00),
    ("Bishan", "Newton"): (0.10, 0.00),
    ("Newton", "Orchard"): (-0.45, 0.00),
    ("Orchard", "Dhoby Ghaut"): (-0.45, 0.00),

    ("Jurong East", "Clementi"): (0.00, 0.10),
    ("Clementi", "Buona Vista"): (0.00, 0.10),
    ("Buona Vista", "City Hall"): (0.00, 0.12),
    ("City Hall", "Bugis"): (0.00, 0.14),
    ("Bugis", "Paya Lebar"): (0.00, 0.10),

    ("HarbourFront", "Buona Vista"): (-0.55, 0.32),
    ("Buona Vista", "Botanic Gardens"): (-0.28, 0.18),
    ("Botanic Gardens", "Bishan"): (0.00, 0.30),
    ("Bishan", "Serangoon"): (0.00, 0.22),
    ("Serangoon", "Promenade"): (0.00, 0.00),

    ("Bukit Panjang", "Beauty World"): (0.00, 0.18),
    ("Beauty World", "King Albert Park"): (0.12, 0.18),
    ("King Albert Park", "Botanic Gardens"): (0.05, 0.22),
    ("Botanic Gardens", "Newton"): (0.00, -0.28),
    ("Newton", "Little India"): (0.10, 0.18),
    ("Little India", "Bugis"): (0.18, -0.26),

    ("HarbourFront", "Outram Park"): (0.18, -0.24),
    ("Outram Park", "Chinatown"): (0.18, -0.22),
    ("Chinatown", "Dhoby Ghaut"): (0.20, 0.18),
    ("Dhoby Ghaut", "Little India"): (0.18, 0.20),
    ("Little India", "Serangoon"): (0.10, 0.24),
    ("Serangoon", "Hougang"): (0.16, 0.18),
}


# =========================
# HELPERS
# =========================
def get_interchange_nodes():
    interchange_nodes = []
    for node in G.nodes():
        lines = set(G[node][n]["line"] for n in G.neighbors(node))
        if len(lines) >= 2:
            interchange_nodes.append(node)
    return interchange_nodes


def get_node_line_colors(node):
    colors = []
    for neighbor in G.neighbors(node):
        color = G[node][neighbor]["color"]
        if color not in colors:
            colors.append(color)
    return colors


def get_node_primary_color(node):
    return get_node_line_colors(node)[0]


def get_midpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)


def normalize_station_name(name):
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def build_station_lookup():
    lookup = {}
    for station in G.nodes():
        lookup[normalize_station_name(station)] = station
    return lookup


STATION_LOOKUP = build_station_lookup()


def resolve_station_input(user_input):
    normalized = normalize_station_name(user_input)

    if normalized in STATION_LOOKUP:
        return STATION_LOOKUP[normalized], []

    partial_matches = []
    for key, value in STATION_LOOKUP.items():
        if normalized and normalized in key:
            partial_matches.append(value)

    if partial_matches:
        return partial_matches[0], []

    suggestions = difflib.get_close_matches(
        normalized,
        list(STATION_LOOKUP.keys()),
        n=3,
        cutoff=0.5
    )

    if suggestions:
        return None, [STATION_LOOKUP[s] for s in suggestions]

    return None, []


def get_line(u, v):
    return G[u][v]["line"]


def build_journey_instructions(path):
    if len(path) < 2:
        return []

    instructions = []
    segment_start = path[0]
    current_line = get_line(path[0], path[1])

    for i in range(1, len(path) - 1):
        next_line = get_line(path[i], path[i + 1])

        if next_line != current_line:
            instructions.append(("ride", current_line, segment_start, path[i]))
            instructions.append(("transfer", path[i], next_line))
            segment_start = path[i]
            current_line = next_line

    instructions.append(("ride", current_line, segment_start, path[-1]))
    return instructions


def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b, alpha)


def find_route(start, end, selected_unit):
    path = nx.shortest_path(G, start, end, weight=selected_unit)

    total_distance = sum(
        G[path[i]][path[i + 1]][selected_unit]
        for i in range(len(path) - 1)
    )

    fare = calculate_fare(total_distance)
    instructions = build_journey_instructions(path)

    return {
        "path": path,
        "distance": total_distance,
        "fare": fare,
        "instructions": instructions,
        "stops": len(path) - 1
    }


# =========================
# TASK 2 
# =========================
def calculate_network_statistics():
    total_km = sum(d["km"] for _, _, d in G.edges(data=True))
    total_miles = sum(d["miles"] for _, _, d in G.edges(data=True))
    total_edges = G.number_of_edges()

    avg_km = total_km / total_edges if total_edges > 0 else 0
    avg_miles = total_miles / total_edges if total_edges > 0 else 0

    return {
        "total_edges": total_edges,
        "total_km": total_km,
        "total_miles": total_miles,
        "avg_km": avg_km,
        "avg_miles": avg_miles
    }


# =========================
# DRAW MAP
# =========================
def draw_manual_edge_labels(ax, selected_unit):
    for u, v, d in G.edges(data=True):
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        mx, my = get_midpoint((x1, y1), (x2, y2))
        dx, dy = edge_label_pos.get((u, v), edge_label_pos.get((v, u), (0, 0)))

        ax.text(
            mx + dx,
            my + dy,
            f"{d[selected_unit]:.1f}",
            fontsize=8,
            fontweight="bold",
            color="#222222",
            ha="center",
            va="center",
            zorder=15,
            bbox=dict(
                facecolor="white",
                edgecolor="#D1D5DB",
                linewidth=0.7,
                alpha=0.95,
                boxstyle="round,pad=0.18"
            )
        )


def draw_station_node(ax, node, radius, alpha=1.0, edge_alpha=1.0):
    x, y = pos[node]
    is_interchange = node in get_interchange_nodes()

    if is_interchange:
        circle = Circle(
            (x, y),
            radius=radius,
            facecolor=(1, 1, 1, alpha),
            edgecolor=(0, 0, 0, edge_alpha),
            linewidth=1.8,
            zorder=6
        )
        ax.add_patch(circle)
        return

    circle = Circle(
        (x, y),
        radius=radius,
        facecolor=hex_to_rgba(get_node_primary_color(node), alpha),
        edgecolor=(1, 1, 1, edge_alpha),
        linewidth=1.4,
        zorder=6
    )
    ax.add_patch(circle)


def draw_all_nodes(ax, route=None):
    normal_radius = 0.34
    interchange_radius = 0.34

    interchange_nodes = set(get_interchange_nodes())
    route_nodes = set(route) if route else set()

    for node in G.nodes():
        if route:
            if node in route_nodes:
                alpha = 1.0
                edge_alpha = 1.0
            else:
                alpha = 0.35
                edge_alpha = 0.35
        else:
            alpha = 1.0
            edge_alpha = 1.0

        radius = interchange_radius if node in interchange_nodes else normal_radius
        draw_station_node(ax, node, radius, alpha=alpha, edge_alpha=edge_alpha)


def create_map_figure(selected_unit="km", route=None):
    unit_label = "KM" if selected_unit == "km" else "MILES"

    fig = Figure(figsize=(17, 10), dpi=100)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    if route:
        route_edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
        route_edges_set = set(tuple(sorted(edge)) for edge in route_edges)

        faded_edges = []
        faded_colors = []
        highlighted_edges = []
        highlighted_colors = []

        for u, v, d in G.edges(data=True):
            edge_key = tuple(sorted((u, v)))
            if edge_key in route_edges_set:
                highlighted_edges.append((u, v))
                highlighted_colors.append(d["color"])
            else:
                faded_edges.append((u, v))
                faded_colors.append(d["color"])

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=faded_edges,
            width=2.4,
            edge_color=faded_colors,
            alpha=0.20,
            ax=ax
        )

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=highlighted_edges,
            width=5.8,
            edge_color=highlighted_colors,
            alpha=1.0,
            ax=ax
        )
    else:
        nx.draw_networkx_edges(
            G,
            pos,
            width=3.0,
            edge_color=[d["color"] for _, _, d in G.edges(data=True)],
            alpha=0.88,
            ax=ax
        )

    draw_all_nodes(ax, route=route)

    if route:
        start_node = route[0]
        end_node = route[-1]

        start_x, start_y = pos[start_node]
        end_x, end_y = pos[end_node]

        interchange_nodes = set(get_interchange_nodes())

        start_radius = 0.48 if start_node in interchange_nodes else 0.34
        end_radius = 0.48 if end_node in interchange_nodes else 0.34

        ax.add_patch(
            Circle(
                (start_x, start_y),
                radius=start_radius,
                facecolor="none",
                edgecolor="#22C55E",
                linewidth=2.6,
                zorder=8
            )
        )

        ax.add_patch(
            Circle(
                (end_x, end_y),
                radius=end_radius,
                facecolor="none",
                edgecolor="#EF4444",
                linewidth=2.6,
                zorder=8
            )
        )

    route_nodes = set(route) if route else set()
    for node, (x, y) in pos.items():
        dx, dy = text_pos.get(node, (0.7, 0.7))
        alpha = 1.0 if (not route or node in route_nodes) else 0.40
        ax.text(
            x + dx,
            y + dy,
            node,
            fontsize=7,
            ha="left",
            va="center",
            zorder=20,
            alpha=alpha
        )

    draw_manual_edge_labels(ax, selected_unit)

    legend_handles = [
        Line2D([0], [0], color="#D42E12", lw=2.8, label="North-South"),
        Line2D([0], [0], color="#009645", lw=2.8, label="East-West"),
        Line2D([0], [0], color="#FA9E0D", lw=2.8, label="Circle"),
        Line2D([0], [0], color="#005EC4", lw=2.8, label="Downtown"),
        Line2D([0], [0], color="#9900AA", lw=2.8, label="North-East"),
        Line2D(
            [0], [0],
            marker="o",
            color="black",
            markerfacecolor="white",
            markeredgecolor="black",
            markeredgewidth=1.4,
            markersize=7,
            lw=0,
            label="Interchange"
        )
    ]

    ax.legend(
        handles=legend_handles,
        loc="upper right",
        fontsize=6.8,
        frameon=True,
        borderpad=0.35,
        labelspacing=0.35,
        handlelength=1.5,
        handletextpad=0.45
    )

    ax.set_title(
        f"Singapore MRT Network ({unit_label})",
        fontsize=15,
        weight="bold",
        pad=8
    )

    x_values = [p[0] for p in pos.values()]
    y_values = [p[1] for p in pos.values()]
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)

    x_pad = 7
    y_pad = 5

    ax.set_xlim(x_min - x_pad, x_max + x_pad)
    ax.set_ylim(y_min - y_pad, y_max + y_pad)

    ax.axis("off")
    fig.subplots_adjust(left=0.015, right=0.99, top=0.90, bottom=0.03)

    return fig


# =========================
# APP
# =========================
class MRTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Singapore MRT Network System")
        self.root.geometry("1680x960")
        self.root.minsize(1380, 820)
        self.root.configure(bg="#F3F6FA")

        self.selected_unit = tk.StringVar(value="km")
        self.start_station = tk.StringVar()
        self.end_station = tk.StringVar()

        self.canvas = None
        self.current_fig = None
        self.last_result = None

        self.setup_styles()
        self.build_gui()
        self.show_full_map()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("TCombobox", font=("Arial", 10))
        style.configure("Action.TButton", font=("Arial", 10, "bold"), padding=(10, 6))
        style.configure("PopupTitle.TLabel", font=("Arial", 14, "bold"))

    def build_gui(self):
        header = tk.Frame(self.root, bg="#F3F6FA")
        header.pack(fill="x", padx=20, pady=(10, 6))

        title = tk.Label(
            header,
            text="SINGAPORE MRT NETWORK SYSTEM",
            font=("Arial", 20, "bold"),
            bg="#F3F6FA",
            fg="#1F2D3D"
        )
        title.pack()

        top_frame = tk.Frame(self.root, bg="#F3F6FA")
        top_frame.pack(fill="x", padx=20, pady=(0, 8))

        control_card = tk.Frame(top_frame, bg="white", bd=1, relief="solid")
        control_card.pack(fill="x")

        control_inner = tk.Frame(control_card, bg="white")
        control_inner.pack(fill="x", padx=12, pady=10)

        left_controls = tk.Frame(control_inner, bg="white")
        left_controls.pack(side="left")

        unit_frame = tk.LabelFrame(
            left_controls,
            text="Unit",
            font=("Arial", 10, "bold"),
            bg="white",
            padx=10,
            pady=6
        )
        unit_frame.pack(side="left", padx=(0, 10))

        tk.Radiobutton(
            unit_frame,
            text="KM",
            variable=self.selected_unit,
            value="km",
            bg="white",
            font=("Arial", 10),
            command=self.refresh_map_only
        ).pack(side="left", padx=6)

        tk.Radiobutton(
            unit_frame,
            text="Miles",
            variable=self.selected_unit,
            value="miles",
            bg="white",
            font=("Arial", 10),
            command=self.refresh_map_only
        ).pack(side="left", padx=6)

        station_frame = tk.LabelFrame(
            left_controls,
            text="Find Route",
            font=("Arial", 10, "bold"),
            bg="white",
            padx=10,
            pady=6
        )
        station_frame.pack(side="left")

        stations = sorted(G.nodes())

        tk.Label(station_frame, text="Start:", bg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=3)
        self.start_combo = ttk.Combobox(
            station_frame,
            textvariable=self.start_station,
            values=stations,
            width=18,
            state="readonly"
        )
        self.start_combo.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(station_frame, text="End:", bg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=3)
        self.end_combo = ttk.Combobox(
            station_frame,
            textvariable=self.end_station,
            values=stations,
            width=18,
            state="readonly"
        )
        self.end_combo.grid(row=0, column=3, padx=5, pady=3)

        self.swap_btn = ttk.Button(
            station_frame,
            text="Swap",
            style="Action.TButton",
            command=self.swap_stations
        )
        self.swap_btn.grid(row=0, column=4, padx=(8, 2), pady=3)

        button_frame = tk.Frame(control_inner, bg="white")
        button_frame.pack(side="right")

        self.clear_btn = ttk.Button(
            button_frame,
            text="Clear",
            style="Action.TButton",
            command=self.clear_selection
        )
        self.clear_btn.pack(side="right", padx=5)

        self.task2_btn = ttk.Button(
            button_frame,
            text="Network Summary",
            style="Action.TButton",
            command=self.show_task2_popup
        )
        self.task2_btn.pack(side="right", padx=5)

        self.full_map_btn = ttk.Button(
            button_frame,
            text="Show Full Map",
            style="Action.TButton",
            command=self.show_full_map
        )
        self.full_map_btn.pack(side="right", padx=5)

        self.find_btn = ttk.Button(
            button_frame,
            text="Find Route",
            style="Action.TButton",
            command=self.find_route_gui
        )
        self.find_btn.pack(side="right", padx=5)

        content = tk.Frame(self.root, bg="#F3F6FA")
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        map_card = tk.Frame(
            content,
            bg="white",
            bd=1,
            relief="solid"
        )
        map_card.pack(fill="both", expand=True)

        map_title = tk.Label(
            map_card,
            text="Map",
            bg="white",
            fg="#1F2D3D",
            font=("Arial", 11, "bold"),
            anchor="w"
        )
        map_title.pack(fill="x", padx=10, pady=(8, 0))

        self.map_container = tk.Frame(map_card, bg="white")
        self.map_container.pack(fill="both", expand=True, padx=6, pady=6)

    def clear_canvas(self):
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        if self.current_fig is not None:
            self.current_fig.clear()
            self.current_fig = None

    def show_figure(self, fig):
        self.clear_canvas()
        self.current_fig = fig
        self.canvas = FigureCanvasTkAgg(fig, master=self.map_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def format_result(self, result):
        unit_label = "KM" if self.selected_unit.get() == "km" else "MILES"
        instructions = result["instructions"]

        step_lines = []
        step = 1
        for item in instructions:
            if item[0] == "ride":
                _, line, from_station, to_station = item
                step_lines.append({
                    "title": f"Step {step}",
                    "text": f"Take {line}\n{from_station} → {to_station}"
                })
            else:
                _, station, next_line = item
                step_lines.append({
                    "title": f"Step {step}",
                    "text": f"Transfer at {station}\nto {next_line}"
                })
            step += 1

        return {
            "route_text": " → ".join(result["path"]),
            "steps": step_lines,
            "stops": result["stops"],
            "distance": f"{result['distance']:.2f} {unit_label}",
            "fare": f"${result['fare']:.2f}"
        }

    def create_info_card(self, parent, title, body, width=420):
        card = tk.Frame(parent, bg="white", bd=1, relief="solid")
        card.pack(fill="x", pady=5)

        inner = tk.Frame(card, bg="white")
        inner.pack(fill="x", padx=10, pady=8)

        title_lbl = tk.Label(
            inner,
            text=title,
            bg="white",
            fg="#111827",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        title_lbl.pack(anchor="w")

        body_lbl = tk.Label(
            inner,
            text=body,
            bg="white",
            fg="#374151",
            font=("Arial", 9),
            justify="left",
            anchor="w",
            wraplength=width
        )
        body_lbl.pack(anchor="w", pady=(4, 0), fill="x")

        return card

    def show_route_popup(self, result):
        popup = tk.Toplevel(self.root)
        popup.title("Route Information")
        popup.geometry("500x420")
        popup.minsize(460, 360)
        popup.configure(bg="#F7F9FC")

        try:
            popup.transient(self.root)
        except Exception:
            pass

        self.root.update_idletasks()

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()

        popup_x = root_x + root_w - 520
        popup_y = root_y + 120
        popup.geometry(f"500x420+{popup_x}+{popup_y}")

        wrapper = tk.Frame(popup, bg="#F7F9FC")
        wrapper.pack(fill="both", expand=True, padx=14, pady=14)

        title = ttk.Label(
            wrapper,
            text="Route Information",
            style="PopupTitle.TLabel",
            background="#F7F9FC"
        )
        title.pack(anchor="w", pady=(0, 8))

        canvas = tk.Canvas(wrapper, bg="#F7F9FC", highlightthickness=0)
        scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#F7F9FC")

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=scrollable, anchor="nw")

        def resize_scrollable(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", resize_scrollable)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        data = self.format_result(result)

        self.create_info_card(scrollable, "Route", data["route_text"], width=420)
        self.create_info_card(
            scrollable,
            "Summary",
            f"Stops: {data['stops']}\nDistance: {data['distance']}\nFare: {data['fare']}",
            width=420
        )

        for step in data["steps"]:
            self.create_info_card(scrollable, step["title"], step["text"], width=420)

        btn_row = tk.Frame(scrollable, bg="#F7F9FC")
        btn_row.pack(fill="x", pady=(8, 0))

        close_btn = ttk.Button(
            btn_row,
            text="Close",
            style="Action.TButton",
            command=popup.destroy
        )
        close_btn.pack(anchor="e")

    def show_task2_popup(self):
        stats = calculate_network_statistics()

        popup = tk.Toplevel(self.root)
        popup.title("Network Summary")
        popup.geometry("460x320")
        popup.resizable(False, False)
        popup.configure(bg="#F7F9FC")

        try:
            popup.transient(self.root)
        except Exception:
            pass

        self.root.update_idletasks()

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()

        popup_x = root_x + root_w - 480
        popup_y = root_y + 140
        popup.geometry(f"460x320+{popup_x}+{popup_y}")

        wrapper = tk.Frame(popup, bg="#F7F9FC")
        wrapper.pack(fill="both", expand=True, padx=16, pady=16)

        title = tk.Label(
            wrapper,
            text="Network Summary",
            bg="#F7F9FC",
            fg="#1F2D3D",
            font=("Arial", 14, "bold")
        )
        title.pack(anchor="w", pady=(0, 10))

        card = tk.Frame(wrapper, bg="white", bd=1, relief="solid")
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg="white")
        inner.pack(fill="both", expand=True, padx=14, pady=14)

        rows = [
            ("Total number of edges", f"{stats['total_edges']}"),
            ("Total network length (KM)", f"{stats['total_km']:.2f}"),
            ("Total network length (Miles)", f"{stats['total_miles']:.2f}"),
            ("Average edge distance (KM)", f"{stats['avg_km']:.2f}"),
            ("Average edge distance (Miles)", f"{stats['avg_miles']:.2f}"),
        ]

        for label, value in rows:
            row = tk.Frame(inner, bg="white")
            row.pack(fill="x", pady=4)

            tk.Label(
                row,
                text=label,
                bg="white",
                fg="#374151",
                font=("Arial", 10),
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=value,
                bg="white",
                fg="#111827",
                font=("Arial", 10, "bold"),
                anchor="e"
            ).pack(side="right")

        close_btn = ttk.Button(
            wrapper,
            text="Close",
            style="Action.TButton",
            command=popup.destroy
        )
        close_btn.pack(anchor="e", pady=(10, 0))

    def draw_route_and_maybe_popup(self, show_popup=True):
        start_input = self.start_station.get().strip()
        end_input = self.end_station.get().strip()

        if not start_input or not end_input:
            return False

        start_station, _ = resolve_station_input(start_input)
        end_station, _ = resolve_station_input(end_input)

        if not start_station or not end_station or start_station == end_station:
            return False

        result = find_route(start_station, end_station, self.selected_unit.get())
        self.last_result = result
        fig = create_map_figure(self.selected_unit.get(), result["path"])
        self.show_figure(fig)

        if show_popup:
            self.show_route_popup(result)
        return True

    def swap_stations(self):
        start = self.start_station.get()
        end = self.end_station.get()
        self.start_station.set(end)
        self.end_station.set(start)

        if self.start_station.get().strip() and self.end_station.get().strip():
            try:
                self.draw_route_and_maybe_popup(show_popup=False)
            except Exception:
                self.show_full_map()

    def find_route_gui(self):
        start_input = self.start_station.get().strip()
        end_input = self.end_station.get().strip()

        if not start_input or not end_input:
            messagebox.showwarning("Missing input", "Please select both Start and End stations.")
            return

        start_station, start_suggestions = resolve_station_input(start_input)
        end_station, end_suggestions = resolve_station_input(end_input)

        if not start_station:
            msg = "Invalid Start station."
            if start_suggestions:
                msg += "\nDid you mean: " + ", ".join(start_suggestions)
            messagebox.showerror("Error", msg)
            return

        if not end_station:
            msg = "Invalid End station."
            if end_suggestions:
                msg += "\nDid you mean: " + ", ".join(end_suggestions)
            messagebox.showerror("Error", msg)
            return

        if start_station == end_station:
            messagebox.showwarning("Invalid selection", "Start and End stations cannot be the same.")
            return

        try:
            self.draw_route_and_maybe_popup(show_popup=True)
        except nx.NetworkXNoPath:
            messagebox.showerror("No route", "No route found between the selected stations.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")

    def show_full_map(self):
        self.last_result = None
        fig = create_map_figure(self.selected_unit.get(), None)
        self.show_figure(fig)

    def refresh_map_only(self):
        start_input = self.start_station.get().strip()
        end_input = self.end_station.get().strip()

        if start_input and end_input and start_input != end_input:
            try:
                self.draw_route_and_maybe_popup(show_popup=False)
                return
            except Exception:
                pass

        self.show_full_map()

    def clear_selection(self):
        self.start_station.set("")
        self.end_station.set("")
        self.last_result = None
        self.show_full_map()


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = MRTApp(root)
    root.mainloop()