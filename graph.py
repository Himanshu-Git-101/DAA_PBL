"""
graph.py - Graph representation using an Adjacency List.
Supports 2D coordinates, 3D spatial elevations, and real GPS coordinates (Latitude & Longitude).
Includes a dedicated Hyderabad logistics network with Amazon Fulfillment Center (Depot).
"""
from typing import Dict, List, Tuple, Optional


class Graph:
    def __init__(self):
        self.adj_list: Dict[str, List[Tuple[str, float]]] = {}
        self.coords: Dict[str, Tuple[float, float, float]] = {}  # (x, y, z)
        self.geo_coords: Dict[str, Dict[str, float]] = {}        # {'lat': float, 'lon': float}
        self.node_types: Dict[str, str] = {}                     # 'Warehouse', 'Tech Hub', etc.

    def add_location(
        self,
        name: str,
        coords: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        geo_coords: Optional[Dict[str, float]] = None,
        node_type: str = "Delivery Point"
    ) -> None:
        """Add a location (vertex) to the graph."""
        if name not in self.adj_list:
            self.adj_list[name] = []
        self.coords[name] = coords
        if geo_coords:
            self.geo_coords[name] = geo_coords
        self.node_types[name] = node_type

    def add_road(self, u: str, v: str, weight: float, bidirectional: bool = True) -> None:
        """Add a weighted road (edge) between location u and location v."""
        if u not in self.adj_list:
            self.add_location(u)
        if v not in self.adj_list:
            self.add_location(v)

        self.adj_list[u].append((v, float(weight)))
        if bidirectional:
            self.adj_list[v].append((u, float(weight)))

    def get_neighbors(self, u: str) -> List[Tuple[str, float]]:
        """Return all outgoing roads from location u."""
        return self.adj_list.get(u, [])

    def get_locations(self) -> List[str]:
        """Return list of all location names."""
        return list(self.adj_list.keys())

    def __repr__(self) -> str:
        """Simple text representation of the adjacency list."""
        lines = []
        for loc, edges in self.adj_list.items():
            edge_str = ", ".join([f"({dest}, {wt} km)" for dest, wt in edges])
            lines.append(f"{loc} -> [{edge_str}]")
        return "\n".join(lines)


def create_sample_city() -> Graph:
    """
    Creates standard 9-location sample city for baseline tests.
    """
    g = Graph()
    nodes = [
        ("Warehouse", (1.0, 5.0, 1.0), {"lat": 17.4447, "lon": 78.4664}, "Warehouse"),
        ("A", (3.0, 7.0, 2.0), {"lat": 17.4375, "lon": 78.4483}, "Junction"),
        ("B", (3.0, 3.0, 2.0), {"lat": 17.4156, "lon": 78.4350}, "Junction"),
        ("C", (5.0, 8.0, 3.0), {"lat": 17.4483, "lon": 78.3915}, "Residential"),
        ("D", (5.0, 4.0, 3.0), {"lat": 17.3916, "lon": 78.4406}, "Commercial"),
        ("E", (7.0, 6.0, 4.0), {"lat": 17.4319, "lon": 78.4073}, "Transit Hub"),
        ("F", (9.0, 5.0, 3.0), {"lat": 17.4504, "lon": 78.3808}, "Suburban"),
        ("G", (7.0, 2.0, 2.0), {"lat": 17.3616, "lon": 78.4747}, "Industrial"),
        ("Customer", (11.0, 5.0, 4.0), {"lat": 17.4401, "lon": 78.3489}, "Customer Hub")
    ]
    for name, coords, geo, ntype in nodes:
        g.add_location(name, coords, geo, ntype)

    edges = [
        ("Warehouse", "A", 5),
        ("Warehouse", "B", 8),
        ("A", "C", 3),
        ("A", "D", 6),
        ("B", "D", 4),
        ("B", "G", 7),
        ("C", "E", 5),
        ("D", "E", 2),
        ("D", "G", 6),
        ("E", "F", 4),
        ("G", "F", 5),
        ("F", "Customer", 3)
    ]
    for u, v, w in edges:
        g.add_road(u, v, w)

    return g


def create_hyderabad_city() -> Graph:
    """
    Creates an authentic Hyderabad metropolitan logistics network.
    Central Warehouse: Amazon Fulfillment Centre (Begumpet / Central Hub)
    Connected to key commercial, residential, and tech districts.
    Includes real Latitude & Longitude coordinates for map tiles.
    """
    g = Graph()
    locations = [
        ("Amazon FC (Begumpet)", (5.0, 5.0, 1.0), {"lat": 17.4447, "lon": 78.4664}, "Amazon Warehouse"),
        ("Hitec City", (2.2, 7.2, 3.8), {"lat": 17.4504, "lon": 78.3808}, "Tech Hub"),
        ("Gachibowli", (1.6, 6.0, 4.2), {"lat": 17.4401, "lon": 78.3489}, "Financial District"),
        ("Madhapur", (3.0, 7.0, 3.5), {"lat": 17.4483, "lon": 78.3915}, "Commercial Hub"),
        ("Jubilee Hills", (3.6, 6.0, 5.0), {"lat": 17.4319, "lon": 78.4073}, "Residential"),
        ("Banjara Hills", (4.2, 5.4, 4.5), {"lat": 17.4156, "lon": 78.4350}, "Premium Residential"),
        ("Ameerpet", (4.8, 6.4, 2.5), {"lat": 17.4375, "lon": 78.4483}, "Commercial Center"),
        ("Secunderabad", (6.4, 7.4, 2.8), {"lat": 17.4399, "lon": 78.4983}, "Transit Hub"),
        ("Charminar", (5.6, 3.0, 2.2), {"lat": 17.3616, "lon": 78.4747}, "Heritage & Retail"),
        ("Koti", (5.8, 4.2, 2.0), {"lat": 17.3850, "lon": 78.4867}, "Retail Market"),
        ("Kukatpally", (2.6, 8.4, 3.2), {"lat": 17.4938, "lon": 78.3999}, "High-Density Residential"),
        ("Uppal", (7.6, 5.6, 2.4), {"lat": 17.4018, "lon": 78.5602}, "Industrial & Logistics"),
        ("Mehdipatnam", (3.8, 4.2, 2.6), {"lat": 17.3916, "lon": 78.4406}, "Transit Junction"),
        ("Woxsen University", (0.5, 9.5, 5.2), {"lat": 17.6585, "lon": 77.8965}, "University Campus"),
        ("Sangareddy", (1.2, 8.8, 4.8), {"lat": 17.6190, "lon": 78.0815}, "District Hub"),
        ("Patancheru", (1.8, 8.0, 4.0), {"lat": 17.5312, "lon": 78.2644}, "Industrial Zone"),
        ("Miyapur", (2.2, 7.8, 3.6), {"lat": 17.4968, "lon": 78.3554}, "Metro Junction"),
        ("Kondapur", (2.0, 7.0, 3.7), {"lat": 17.4682, "lon": 78.3582}, "Residential"),
        ("Nanakramguda", (1.4, 5.4, 4.0), {"lat": 17.4190, "lon": 78.3418}, "Financial Phase 2"),
        ("Dilsukhnagar", (6.8, 3.8, 2.1), {"lat": 17.3688, "lon": 78.5247}, "Commercial Market"),
        ("LB Nagar", (7.2, 3.2, 2.2), {"lat": 17.3457, "lon": 78.5522}, "Transit Hub"),
        ("Shamshabad (RGIA)", (3.6, 1.0, 2.0), {"lat": 17.2403, "lon": 78.4294}, "Airport Hub")
    ]
    for name, coords, geo, ntype in locations:
        g.add_location(name, coords, geo, ntype)

    roads = [
        ("Woxsen University", "Sangareddy", 24),
        ("Sangareddy", "Patancheru", 18),
        ("Patancheru", "Miyapur", 12),
        ("Miyapur", "Kukatpally", 7),
        ("Miyapur", "Kondapur", 6),
        ("Kondapur", "Hitec City", 4),
        ("Kondapur", "Gachibowli", 5),
        ("Amazon FC (Begumpet)", "Ameerpet", 3),
        ("Amazon FC (Begumpet)", "Secunderabad", 5),
        ("Amazon FC (Begumpet)", "Banjara Hills", 4),
        ("Amazon FC (Begumpet)", "Koti", 6),
        ("Ameerpet", "Madhapur", 6),
        ("Madhapur", "Hitec City", 3),
        ("Hitec City", "Gachibowli", 4),
        ("Gachibowli", "Nanakramguda", 3),
        ("Gachibowli", "Jubilee Hills", 5),
        ("Madhapur", "Jubilee Hills", 4),
        ("Jubilee Hills", "Banjara Hills", 3),
        ("Hitec City", "Kukatpally", 5),
        ("Ameerpet", "Kukatpally", 6),
        ("Banjara Hills", "Mehdipatnam", 4),
        ("Mehdipatnam", "Charminar", 5),
        ("Mehdipatnam", "Shamshabad (RGIA)", 18),
        ("Charminar", "Shamshabad (RGIA)", 15),
        ("Charminar", "Koti", 3),
        ("Koti", "Dilsukhnagar", 5),
        ("Dilsukhnagar", "LB Nagar", 4),
        ("LB Nagar", "Uppal", 7),
        ("Koti", "Secunderabad", 6),
        ("Secunderabad", "Uppal", 7),
        ("Koti", "Uppal", 6),
        ("Mehdipatnam", "Gachibowli", 8)
    ]
    for u, v, w in roads:
        g.add_road(u, v, w)

    return g
