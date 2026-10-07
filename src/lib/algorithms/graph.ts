import { Location, RoadEdge } from '../../types';

export class LogisticsGraph {
  private adjacencyList: Map<string, Array<{ to: string; distanceKm: number; travelMinutes: number }>> = new Map();
  private locations: Map<string, Location> = new Map();
  private edgesList: RoadEdge[] = [];

  constructor() {
    this.adjacencyList = new Map();
    this.locations = new Map();
    this.edgesList = [];
  }

  addLocation(location: Location): void {
    this.locations.set(location.id, location);
    if (!this.adjacencyList.has(location.id)) {
      this.adjacencyList.set(location.id, []);
    }
  }

  addRoad(from: string, to: string, distanceKm: number, speedKmH: number = 32, bidirectional: boolean = true): void {
    // derive travel minutes from speed assumption: (dist / speed) * 60
    const travelMinutes = Math.round((distanceKm / speedKmH) * 60 * 10) / 10;

    if (!this.locations.has(from) || !this.locations.has(to)) {
      return;
    }

    const outgoing = this.adjacencyList.get(from) || [];
    outgoing.push({ to, distanceKm, travelMinutes });
    this.adjacencyList.set(from, outgoing);

    this.edgesList.push({
      from,
      to,
      distanceKm,
      travelMinutes,
      bidirectional
    });

    if (bidirectional) {
      const incoming = this.adjacencyList.get(to) || [];
      incoming.push({ to: from, distanceKm, travelMinutes });
      this.adjacencyList.set(to, incoming);
    }
  }

  getNeighbors(locationId: string): Array<{ to: string; distanceKm: number; travelMinutes: number }> {
    return this.adjacencyList.get(locationId) || [];
  }

  getLocation(locationId: string): Location | undefined {
    return this.locations.get(locationId);
  }

  getAllLocations(): Location[] {
    return Array.from(this.locations.values());
  }

  getAllEdges(): RoadEdge[] {
    return this.edgesList;
  }

  getAdjacencyList(): Map<string, Array<{ to: string; distanceKm: number; travelMinutes: number }>> {
    return this.adjacencyList;
  }
}

/**
 * Hyderabad metropolitan logistics graph with Main Parcel Warehouse as Central Depot,
 * extended with Woxsen University and major Greater Hyderabad logistic corridors.
 */
export function createHyderabadNetwork(): LogisticsGraph {
  const g = new LogisticsGraph();

  const hyderabadLocations: Location[] = [
    {
      id: "Main Parcel Warehouse",
      name: "Main Parcel Warehouse",
      area: "Begumpet Central Logistics Hub",
      lat: 17.4447,
      lng: 78.4664,
      kind: "depot",
      x: 5.0,
      y: 5.0,
      z: 1.0
    },
    {
      id: "Woxsen University",
      name: "Woxsen University",
      area: "Kamkole / Sangareddy NH65",
      lat: 17.6585,
      lng: 77.8965,
      kind: "drop",
      x: 0.5,
      y: 9.5,
      z: 5.2
    },
    {
      id: "Sangareddy",
      name: "Sangareddy",
      area: "District Transit Corridor",
      lat: 17.6190,
      lng: 78.0815,
      kind: "hub",
      x: 1.2,
      y: 8.8,
      z: 4.8
    },
    {
      id: "Patancheru",
      name: "Patancheru",
      area: "Industrial Logistics Zone",
      lat: 17.5312,
      lng: 78.2644,
      kind: "pickup",
      x: 1.8,
      y: 8.0,
      z: 4.0
    },
    {
      id: "Miyapur",
      name: "Miyapur",
      area: "Metro Transit Corridor",
      lat: 17.4968,
      lng: 78.3554,
      kind: "hub",
      x: 2.2,
      y: 7.8,
      z: 3.6
    },
    {
      id: "Kondapur",
      name: "Kondapur",
      area: "IT Commercial & Residential",
      lat: 17.4682,
      lng: 78.3582,
      kind: "drop",
      x: 2.0,
      y: 7.0,
      z: 3.7
    },
    {
      id: "Hitec City",
      name: "Hitec City",
      area: "Cyberabad Tech Corridor",
      lat: 17.4504,
      lng: 78.3808,
      kind: "drop",
      x: 2.2,
      y: 6.8,
      z: 3.8
    },
    {
      id: "Gachibowli",
      name: "Gachibowli",
      area: "Financial District",
      lat: 17.4401,
      lng: 78.3489,
      kind: "drop",
      x: 1.6,
      y: 6.0,
      z: 4.2
    },
    {
      id: "Nanakramguda",
      name: "Nanakramguda",
      area: "Financial District Phase 2",
      lat: 17.4190,
      lng: 78.3418,
      kind: "drop",
      x: 1.4,
      y: 5.4,
      z: 4.0
    },
    {
      id: "Madhapur",
      name: "Madhapur",
      area: "Commercial & IT Hub",
      lat: 17.4483,
      lng: 78.3915,
      kind: "pickup",
      x: 3.0,
      y: 7.0,
      z: 3.5
    },
    {
      id: "Jubilee Hills",
      name: "Jubilee Hills",
      area: "Residential Hills",
      lat: 17.4319,
      lng: 78.4073,
      kind: "drop",
      x: 3.6,
      y: 6.0,
      z: 5.0
    },
    {
      id: "Banjara Hills",
      name: "Banjara Hills",
      area: "Commercial & Medical Zone",
      lat: 17.4156,
      lng: 78.4350,
      kind: "pickup",
      x: 4.2,
      y: 5.4,
      z: 4.5
    },
    {
      id: "Ameerpet",
      name: "Ameerpet",
      area: "Central Transit Junction",
      lat: 17.4375,
      lng: 78.4483,
      kind: "hub",
      x: 4.8,
      y: 6.4,
      z: 2.5
    },
    {
      id: "Secunderabad",
      name: "Secunderabad",
      area: "Railway Hub & North Zone",
      lat: 17.4399,
      lng: 78.4983,
      kind: "pickup",
      x: 6.4,
      y: 7.4,
      z: 2.8
    },
    {
      id: "Charminar",
      name: "Charminar",
      area: "Old City & Retail Markets",
      lat: 17.3616,
      lng: 78.4747,
      kind: "drop",
      x: 5.6,
      y: 3.0,
      z: 2.2
    },
    {
      id: "Koti",
      name: "Koti",
      area: "Trading & Wholesale Hub",
      lat: 17.3850,
      lng: 78.4867,
      kind: "pickup",
      x: 5.8,
      y: 4.2,
      z: 2.0
    },
    {
      id: "Dilsukhnagar",
      name: "Dilsukhnagar",
      area: "Commercial Retail Hub",
      lat: 17.3688,
      lng: 78.5247,
      kind: "drop",
      x: 6.8,
      y: 3.8,
      z: 2.1
    },
    {
      id: "LB Nagar",
      name: "LB Nagar",
      area: "Southeast Logistics Hub",
      lat: 17.3457,
      lng: 78.5522,
      kind: "hub",
      x: 7.2,
      y: 3.2,
      z: 2.2
    },
    {
      id: "Kukatpally",
      name: "Kukatpally",
      area: "High Density Residential",
      lat: 17.4938,
      lng: 78.3999,
      kind: "drop",
      x: 2.6,
      y: 8.4,
      z: 3.2
    },
    {
      id: "Uppal",
      name: "Uppal",
      area: "Industrial Corridor",
      lat: 17.4018,
      lng: 78.5602,
      kind: "drop",
      x: 7.6,
      y: 5.6,
      z: 2.4
    },
    {
      id: "Mehdipatnam",
      name: "Mehdipatnam",
      area: "Southwest Highway Gateway",
      lat: 17.3916,
      lng: 78.4406,
      kind: "hub",
      x: 3.8,
      y: 4.2,
      z: 2.6
    },
    {
      id: "Shamshabad (RGIA)",
      name: "Shamshabad (RGIA)",
      area: "Airport Cargo & Air Logistics",
      lat: 17.2403,
      lng: 78.4294,
      kind: "pickup",
      x: 3.6,
      y: 1.0,
      z: 2.0
    }
  ];

  hyderabadLocations.forEach(loc => g.addLocation(loc));

  // Connected road network (distances in km, speeds 32 km/h)
  const roads: Array<[string, string, number]> = [
    // Woxsen corridor via NH65
    ["Woxsen University", "Sangareddy", 24.0],
    ["Sangareddy", "Patancheru", 18.0],
    ["Patancheru", "Miyapur", 12.0],
    ["Miyapur", "Kukatpally", 7.0],
    ["Miyapur", "Kondapur", 6.0],

    // IT Corridor
    ["Kondapur", "Hitec City", 4.0],
    ["Kondapur", "Gachibowli", 5.0],
    ["Hitec City", "Gachibowli", 4.0],
    ["Gachibowli", "Nanakramguda", 3.0],
    ["Hitec City", "Madhapur", 3.0],
    ["Hitec City", "Kukatpally", 5.0],

    // Central & Depot Hub
    ["Main Parcel Warehouse", "Ameerpet", 3.0],
    ["Main Parcel Warehouse", "Secunderabad", 5.0],
    ["Main Parcel Warehouse", "Banjara Hills", 4.0],
    ["Main Parcel Warehouse", "Koti", 6.0],
    ["Ameerpet", "Madhapur", 6.0],
    ["Ameerpet", "Kukatpally", 6.0],

    // Hills
    ["Banjara Hills", "Jubilee Hills", 3.0],
    ["Jubilee Hills", "Madhapur", 4.0],
    ["Jubilee Hills", "Gachibowli", 5.0],
    ["Banjara Hills", "Mehdipatnam", 4.0],

    // South & Airport
    ["Mehdipatnam", "Gachibowli", 8.0],
    ["Mehdipatnam", "Charminar", 5.0],
    ["Mehdipatnam", "Shamshabad (RGIA)", 18.0],
    ["Charminar", "Shamshabad (RGIA)", 15.0],
    ["Charminar", "Koti", 3.0],

    // East & Industrial
    ["Koti", "Dilsukhnagar", 5.0],
    ["Dilsukhnagar", "LB Nagar", 4.0],
    ["LB Nagar", "Uppal", 7.0],
    ["Koti", "Secunderabad", 6.0],
    ["Koti", "Uppal", 6.0],
    ["Secunderabad", "Uppal", 7.0]
  ];

  roads.forEach(([u, v, dist]) => g.addRoad(u, v, dist, 32));

  return g;
}
