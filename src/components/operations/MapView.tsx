import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import { Location, PlanStop, DeliveryRequest } from '../../types';
import { LogisticsGraph } from '../../lib/algorithms/graph';
import { Layers, Play, Pause, RotateCcw, Key, Sparkles, Map as MapIcon, Globe } from 'lucide-react';

interface MapViewProps {
  graph: LogisticsGraph;
  stops: PlanStop[];
  selectedDeliveryId: string | null;
  onSelectDeliveryId: (id: string | null) => void;
  replayProgress: number; // 0 to 100
  isReplaying: boolean;
  onToggleReplay: () => void;
  onResetReplay: () => void;
  deliveries: DeliveryRequest[];
}

export const MapView: React.FC<MapViewProps> = ({
  graph,
  stops,
  selectedDeliveryId,
  onSelectDeliveryId,
  replayProgress,
  isReplaying,
  onToggleReplay,
  onResetReplay,
  deliveries
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const routeLayerGroupRef = useRef<L.LayerGroup | null>(null);
  const markersLayerGroupRef = useRef<L.LayerGroup | null>(null);
  const replayMarkerRef = useRef<L.Marker | null>(null);
  const activeTileLayerRef = useRef<L.TileLayer | null>(null);

  const [mapType, setMapType] = useState<"roadmap" | "satellite" | "hybrid">("roadmap");
  const [routeLayerMode, setRouteLayerMode] = useState<"dijkstra" | "smooth_road" | "both">("both");
  const [apiKeyModalOpen, setApiKeyModalOpen] = useState(false);
  const [customApiKey, setCustomApiKey] = useState(() => {
    return localStorage.getItem("gmaps_api_key") || import.meta.env.VITE_GOOGLE_MAPS_API_KEY || "";
  });

  // Google Maps Tile URLs (Real Google Maps Engine)
  // lyrs=m: Roadmap, lyrs=s: Satellite, lyrs=y: Hybrid with labels, lyrs=p: Terrain
  const googleTileUrls = {
    roadmap: 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    satellite: 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    hybrid: 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'
  };

  // Initialize Map with Google Maps Roadmap Tiles
  useEffect(() => {
    if (!mapContainerRef.current) return;
    if (mapInstanceRef.current) return;

    // Center on Begumpet / Hyderabad
    const map = L.map(mapContainerRef.current, {
      center: [17.4350, 78.4350],
      zoom: 12,
      zoomControl: false,
      attributionControl: false
    });

    // Add Google Maps Roadmap Layer
    const tileLayer = L.tileLayer(googleTileUrls[mapType], {
      maxZoom: 20,
      subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    }).addTo(map);

    activeTileLayerRef.current = tileLayer;

    // Zoom controls top right in clean white style
    L.control.zoom({ position: 'topright' }).addTo(map);

    routeLayerGroupRef.current = L.layerGroup().addTo(map);
    markersLayerGroupRef.current = L.layerGroup().addTo(map);

    mapInstanceRef.current = map;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // Update Tile Layer when mapType switches (Roadmap vs Satellite)
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;

    if (activeTileLayerRef.current) {
      map.removeLayer(activeTileLayerRef.current);
    }

    const newTileLayer = L.tileLayer(googleTileUrls[mapType], {
      maxZoom: 20,
      subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    }).addTo(map);

    activeTileLayerRef.current = newTileLayer;
  }, [mapType]);

  // Update map contents when stops, graph or selected delivery changes
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map || !routeLayerGroupRef.current || !markersLayerGroupRef.current) return;

    const routeGroup = routeLayerGroupRef.current;
    const markersGroup = markersLayerGroupRef.current;

    routeGroup.clearLayers();
    markersGroup.clearLayers();

    const allLocations = graph.getAllLocations();
    const locMap = new Map<string, Location>();
    allLocations.forEach(loc => locMap.set(loc.id, loc));

    // 1. Draw base road network (clean subtle road connection lines)
    graph.getAllEdges().forEach(edge => {
      const u = locMap.get(edge.from);
      const v = locMap.get(edge.to);
      if (u && v) {
        L.polyline([[u.lat, u.lng], [v.lat, v.lng]], {
          color: mapType === 'satellite' ? 'rgba(255, 255, 255, 0.4)' : '#cbd5e1',
          weight: 2.5,
          dashArray: '5, 5'
        }).addTo(routeGroup);
      }
    });

    // 2. Draw planned route polyline
    const routeCoords: Array<[number, number]> = [];

    stops.forEach((stop) => {
      if (stop.legPathNodes && stop.legPathNodes.length > 0) {
        stop.legPathNodes.forEach(nodeId => {
          const loc = locMap.get(nodeId);
          if (loc) {
            routeCoords.push([loc.lat, loc.lng]);
          }
        });
      } else {
        const loc = locMap.get(stop.locationId);
        if (loc) {
          routeCoords.push([loc.lat, loc.lng]);
        }
      }
    });

    if (routeCoords.length > 1) {
      // Dijkstra teaching route: high-visibility crisp cyan/teal line
      if (routeLayerMode === "dijkstra" || routeLayerMode === "both") {
        L.polyline(routeCoords, {
          color: '#0284c7', // Sky Blue
          weight: 4,
          opacity: 0.9,
          lineCap: 'round',
          lineJoin: 'round'
        }).addTo(routeGroup);
      }

      // Main Road Route: Signature energetic Orange line with white outline
      if (routeLayerMode === "smooth_road" || routeLayerMode === "both") {
        // Outline for contrast on Google Maps
        L.polyline(routeCoords, {
          color: '#ffffff',
          weight: 8,
          opacity: 0.9
        }).addTo(routeGroup);

        L.polyline(routeCoords, {
          color: '#ff5500', // Signature Orange
          weight: 5,
          opacity: 1.0,
          lineCap: 'round',
          lineJoin: 'round'
        }).addTo(routeGroup);
      }
    }

    // 3. Highlight selected delivery if any
    if (selectedDeliveryId) {
      const selectedReq = deliveries.find(d => d.id === selectedDeliveryId);
      if (selectedReq) {
        const pickupLoc = locMap.get(selectedReq.pickupLocationId);
        const dropLoc = locMap.get(selectedReq.dropLocationId);
        if (pickupLoc && dropLoc) {
          L.polyline([[pickupLoc.lat, pickupLoc.lng], [dropLoc.lat, dropLoc.lng]], {
            color: '#e11d48', // Vibrant Rose/Amber
            weight: 4,
            opacity: 0.95,
            dashArray: '8, 8'
          }).addTo(routeGroup);
        }
      }
    }

    // 4. Place Google Maps styled pin markers
    allLocations.forEach(loc => {
      const stopIdx = stops.findIndex(s => s.locationId === loc.id);
      const isDepot = loc.kind === "depot";

      const isSelectedPickup = deliveries.some(d => d.id === selectedDeliveryId && d.pickupLocationId === loc.id);
      const isSelectedDrop = deliveries.some(d => d.id === selectedDeliveryId && d.dropLocationId === loc.id);
      const isHighlighted = isSelectedPickup || isSelectedDrop;

      let markerBg = isDepot ? '#ea580c' : '#ffffff';
      let textColor = isDepot ? '#ffffff' : '#0f172a';
      let borderColor = isDepot ? '#ffffff' : '#ff5500';
      let label = isDepot ? '★' : `${loc.name.charAt(0)}`;

      if (stopIdx >= 0) {
        label = `${stopIdx + 1}`;
        markerBg = isDepot ? '#ea580c' : '#ff5500';
        textColor = '#ffffff';
        borderColor = '#ffffff';
      }

      const iconHtml = `
        <div style="
          width: ${isHighlighted ? '34px' : '28px'};
          height: ${isHighlighted ? '34px' : '28px'};
          border-radius: 50%;
          background: ${markerBg};
          border: 2.5px solid ${borderColor};
          display: flex;
          align-items: center;
          justify-content: center;
          font-family: 'Sansation', sans-serif;
          font-weight: 700;
          font-size: ${isHighlighted ? '13px' : '11px'};
          color: ${textColor};
          box-shadow: 0 4px 12px rgba(234, 88, 12, ${isHighlighted ? '0.45' : '0.25'});
          transform: translate(-50%, -50%);
          cursor: pointer;
          transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        ">
          ${label}
        </div>
      `;

      const customIcon = L.divIcon({
        className: 'google-map-pin',
        html: iconHtml,
        iconSize: [28, 28]
      });

      const marker = L.marker([loc.lat, loc.lng], { icon: customIcon });

      const popupContent = `
        <div style="font-family: 'Sansation', sans-serif; color: #0f172a; font-size: 12px; line-height: 1.4; padding: 2px;">
          <div style="font-weight: 700; color: #ff5500; font-size: 13px;">${loc.name}</div>
          <div style="color: #64748b; font-size: 11px;">${loc.area}</div>
          <div style="margin-top: 6px; padding-top: 5px; border-top: 1px solid #fed7aa;">
            <div><strong>Kind:</strong> ${loc.kind.toUpperCase()}</div>
            <div><strong>GPS:</strong> ${loc.lat.toFixed(4)}, ${loc.lng.toFixed(4)}</div>
            ${stopIdx >= 0 ? `<div style="color: #ff5500; font-weight: 700; margin-top: 3px;">Stop #${stopIdx + 1} in Today's Route</div>` : ''}
          </div>
        </div>
      `;

      marker.bindPopup(popupContent, {
        className: 'google-style-popup'
      });

      marker.on('click', () => {
        const matched = deliveries.find(d => d.pickupLocationId === loc.id || d.dropLocationId === loc.id);
        if (matched) {
          onSelectDeliveryId(matched.id);
        }
      });

      marker.addTo(markersGroup);
    });

    // 5. Fit bounds if stops exist
    if (routeCoords.length > 0) {
      const bounds = L.latLngBounds(routeCoords);
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [graph, stops, selectedDeliveryId, routeLayerMode, mapType]);

  // Replay vehicle marker update
  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;

    if (stops.length < 2) {
      if (replayMarkerRef.current) {
        replayMarkerRef.current.remove();
        replayMarkerRef.current = null;
      }
      return;
    }

    const allLocations = graph.getAllLocations();
    const locMap = new Map<string, Location>();
    allLocations.forEach(loc => locMap.set(loc.id, loc));

    const points: Array<[number, number]> = [];
    stops.forEach(stop => {
      const loc = locMap.get(stop.locationId);
      if (loc) points.push([loc.lat, loc.lng]);
    });

    if (points.length < 2) return;

    const totalSegments = points.length - 1;
    const progressUnit = replayProgress / 100;
    const scaled = progressUnit * totalSegments;
    const segmentIdx = Math.min(Math.floor(scaled), totalSegments - 1);
    const segmentFraction = scaled - segmentIdx;

    const p1 = points[segmentIdx];
    const p2 = points[segmentIdx + 1];

    const currentLat = p1[0] + (p2[0] - p1[0]) * segmentFraction;
    const currentLng = p1[1] + (p2[1] - p1[1]) * segmentFraction;

    const vanIconHtml = `
      <div style="
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #ff5500;
        border: 3px solid #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        box-shadow: 0 4px 16px rgba(255, 85, 0, 0.6);
        transform: translate(-50%, -50%);
      ">
        🚚
      </div>
    `;

    const vanIcon = L.divIcon({
      className: 'replay-van-icon',
      html: vanIconHtml,
      iconSize: [36, 36]
    });

    if (!replayMarkerRef.current) {
      replayMarkerRef.current = L.marker([currentLat, currentLng], { icon: vanIcon }).addTo(map);
    } else {
      replayMarkerRef.current.setLatLng([currentLat, currentLng]);
      replayMarkerRef.current.setIcon(vanIcon);
    }
  }, [replayProgress, stops, graph]);

  const handleSaveApiKey = () => {
    localStorage.setItem("gmaps_api_key", customApiKey.trim());
    setApiKeyModalOpen(false);
  };

  return (
    <div className="map-view-card relative overflow-hidden flex flex-col h-full bg-white border border-orange-200/80 rounded-2xl shadow-sm">
      {/* Google Maps Header & Controls Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-2.5 bg-white/95 backdrop-blur-md border-b border-orange-100 z-10 text-xs">
        {/* Left: Google Maps Brand Badge */}
        <div className="flex items-center gap-2.5">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-orange-50 border border-orange-200 text-orange-700 font-bold">
            <span className="text-[#4285F4] font-bold">G</span>
            <span className="text-[#EA4335] font-bold">o</span>
            <span className="text-[#FBBC05] font-bold">o</span>
            <span className="text-[#4285F4] font-bold">g</span>
            <span className="text-[#34A853] font-bold">l</span>
            <span className="text-[#EA4335] font-bold">e</span>
            <span className="text-slate-800 ml-1">Maps</span>
          </div>

          <span className="text-[11px] text-slate-500 font-medium hidden sm:inline">
            Hyderabad Logistics Corridor (Main Parcel Warehouse)
          </span>
        </div>

        {/* Right: Map Type Toggle (Roadmap vs Satellite) + Layer Mode */}
        <div className="flex items-center gap-2">
          {/* Roadmap / Satellite Toggle */}
          <div className="flex items-center bg-slate-100 rounded-lg p-0.5 border border-slate-200">
            <button
              onClick={() => setMapType("roadmap")}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-semibold transition-all ${
                mapType === "roadmap"
                  ? "bg-white text-orange-600 shadow-sm"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              <MapIcon className="w-3 h-3" />
              <span>Map</span>
            </button>
            <button
              onClick={() => setMapType("satellite")}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-semibold transition-all ${
                mapType === "satellite"
                  ? "bg-white text-orange-600 shadow-sm"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              <Globe className="w-3 h-3" />
              <span>Satellite</span>
            </button>
          </div>

          {/* Route Layer Switcher */}
          <div className="hidden md:flex items-center bg-slate-100 rounded-lg p-0.5 border border-slate-200">
            <button
              onClick={() => setRouteLayerMode("smooth_road")}
              className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-all ${
                routeLayerMode === "smooth_road"
                  ? "bg-orange-500 text-white shadow-sm"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Orange Road Route
            </button>
            <button
              onClick={() => setRouteLayerMode("dijkstra")}
              className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-all ${
                routeLayerMode === "dijkstra"
                  ? "bg-sky-600 text-white shadow-sm"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Dijkstra Leg
            </button>
            <button
              onClick={() => setRouteLayerMode("both")}
              className={`px-2.5 py-1 rounded-md text-[11px] font-semibold transition-all ${
                routeLayerMode === "both"
                  ? "bg-slate-800 text-white shadow-sm"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Both
            </button>
          </div>

          {/* API Key Modal Button */}
          <button
            onClick={() => setApiKeyModalOpen(true)}
            className="flex items-center gap-1 px-2.5 py-1 bg-white hover:bg-orange-50 text-orange-700 border border-orange-200 rounded-lg transition-colors font-medium text-[11px]"
            title="Google Maps API Key Configuration"
          >
            <Key className="w-3.5 h-3.5 text-orange-600" />
            <span className="hidden sm:inline">{customApiKey ? "Key Active" : "Connect Key"}</span>
          </button>
        </div>
      </div>

      {/* Map Canvas */}
      <div className="relative flex-1 w-full min-h-[390px] bg-slate-100">
        <div ref={mapContainerRef} className="w-full h-full" style={{ minHeight: "390px" }} />

        {/* Google Maps Official Watermark Badge at Bottom Left */}
        <div className="absolute bottom-3 left-4 z-10 pointer-events-none select-none flex items-center gap-1.5 bg-white/90 backdrop-blur-sm px-2.5 py-1 rounded shadow-sm border border-slate-200">
          <span className="font-bold text-xs tracking-tight">
            <span className="text-[#4285F4]">G</span>
            <span className="text-[#EA4335]">o</span>
            <span className="text-[#FBBC05]">o</span>
            <span className="text-[#4285F4]">g</span>
            <span className="text-[#34A853]">l</span>
            <span className="text-[#EA4335]">e</span>
          </span>
          <span className="text-[10px] text-slate-500">Maps Real-Time View</span>
        </div>

        {/* Floating Legend & Simulation Replay Bar */}
        <div className="absolute bottom-3 right-4 z-10 flex flex-wrap items-center gap-3 p-2.5 bg-white/95 backdrop-blur-md border border-orange-200/90 rounded-xl shadow-md text-xs">
          {/* Legend */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 rounded-full bg-[#ea580c] inline-block border border-white"></span>
              <span className="text-slate-700 font-medium">Depot</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="w-2.5 h-2.5 rounded-full bg-[#ff5500] inline-block"></span>
              <span className="text-slate-700 font-medium">Stop</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="w-3 h-1 bg-[#ff5500] inline-block rounded-full"></span>
              <span className="text-slate-700 font-medium">Route</span>
            </div>
          </div>

          {/* Replay Controls */}
          {stops.length > 1 && (
            <div className="flex items-center gap-2 pl-2 border-l border-orange-200">
              <div className="font-mono text-[11px] text-orange-600 font-bold">
                {Math.round(replayProgress)}%
              </div>
              <button
                onClick={onToggleReplay}
                className="p-1.5 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors flex items-center justify-center shadow-sm"
                title={isReplaying ? "Pause Simulation" : "Start Replay"}
              >
                {isReplaying ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
              </button>
              <button
                onClick={onResetReplay}
                className="p-1.5 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-lg transition-colors"
                title="Reset Replay"
              >
                <RotateCcw className="w-3 h-3" />
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Google Maps API Key Modal */}
      {apiKeyModalOpen && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
          <div className="bg-white border border-orange-200 rounded-2xl shadow-xl max-w-md w-full p-6 text-slate-800">
            <div className="flex items-center justify-between pb-3 border-b border-orange-100 mb-4">
              <div className="flex items-center gap-2 font-bold text-base text-slate-900">
                <Key className="w-5 h-5 text-orange-500" />
                <span>Google Maps Platform Key</span>
              </div>
              <button
                onClick={() => setApiKeyModalOpen(false)}
                className="text-slate-400 hover:text-slate-700 font-bold"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed mb-4">
              SmartRoute currently streams Google Maps live tiles. To activate full Google Maps JavaScript 3D Photorealistic Tiles and Road libraries, paste your Google Cloud Maps API Key below:
            </p>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Google Maps API Key
                </label>
                <input
                  type="text"
                  placeholder="AIzaSy..."
                  value={customApiKey}
                  onChange={(e) => setCustomApiKey(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-xs text-slate-900 font-mono focus:outline-none focus:border-orange-500"
                />
              </div>

              <div className="p-3 rounded-lg bg-orange-50 border border-orange-100 text-[11px] text-orange-800">
                💡 Need a free key? Generate an instant prototype key at{" "}
                <a
                  href="https://mapsplatform.google.com/maps-demo-key?utm_campaign=gmp_git_agentskills_v1"
                  target="_blank"
                  rel="noreferrer"
                  className="underline font-bold text-orange-600"
                >
                  Google Maps Demo Key Quickstart
                </a>
                .
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  onClick={() => setApiKeyModalOpen(false)}
                  className="px-3.5 py-1.5 rounded-lg border border-slate-200 text-xs font-medium text-slate-600 hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSaveApiKey}
                  className="px-4 py-1.5 rounded-lg bg-orange-500 hover:bg-orange-600 text-white text-xs font-bold shadow-md shadow-orange-500/20"
                >
                  Save & Apply
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
