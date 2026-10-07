import React, { useState } from 'react';
import { DeliveryRequest, Location } from '../../types';
import { X, PlusCircle, AlertTriangle } from 'lucide-react';

interface DeliveryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAddDelivery: (newDelivery: DeliveryRequest) => void;
  locations: Location[];
}

export const DeliveryModal: React.FC<DeliveryModalProps> = ({
  isOpen,
  onClose,
  onAddDelivery,
  locations
}) => {
  const [pickup, setPickup] = useState(locations[1]?.id || "");
  const [drop, setDrop] = useState(locations[2]?.id || "");
  const [weightKg, setWeightKg] = useState<string>("6.5");
  const [profit, setProfit] = useState<string>("550");
  const [deadlineMinutes, setDeadlineMinutes] = useState<string>("240");
  const [packageType, setPackageType] = useState<string>("Express Parcel");
  const [priority, setPriority] = useState<"HIGH" | "MEDIUM" | "LOW">("HIGH");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);

    const parsedWeight = parseFloat(weightKg);
    const parsedProfit = parseFloat(profit);
    const parsedDeadline = parseInt(deadlineMinutes, 10);

    if (pickup === drop) {
      setErrorMsg("Pickup and Drop locations must be distinct nodes.");
      return;
    }
    if (isNaN(parsedWeight) || parsedWeight <= 0) {
      setErrorMsg("Package weight must be a positive number.");
      return;
    }
    if (isNaN(parsedProfit) || parsedProfit <= 0) {
      setErrorMsg("Profit must be a positive number.");
      return;
    }
    if (isNaN(parsedDeadline) || parsedDeadline <= 0) {
      setErrorMsg("Deadline minutes must be greater than zero.");
      return;
    }

    const newDelivery: DeliveryRequest = {
      id: `DEL-${Math.floor(100 + Math.random() * 900)}`,
      pickupLocationId: pickup,
      dropLocationId: drop,
      weightKg: Math.round(parsedWeight * 10) / 10,
      profit: Math.round(parsedProfit),
      deadlineMinutesFromStart: parsedDeadline,
      priority,
      status: "pending",
      packageType: packageType.trim() || "Standard Box",
      riskLevel: "SAFE"
    };

    onAddDelivery(newDelivery);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-md bg-white border-2 border-orange-200 rounded-2xl shadow-2xl p-6 text-slate-800">
        <div className="flex items-center justify-between pb-3 border-b border-orange-100">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-orange-100 text-orange-600 flex items-center justify-center">
              <PlusCircle className="w-5 h-5" />
            </div>
            <h2 className="text-base font-bold text-slate-900">Create Delivery Request</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-slate-400 hover:text-slate-800 rounded-lg hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {errorMsg && (
          <div className="mt-4 p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-500 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-4 space-y-3.5 text-xs">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-slate-700 mb-1 font-bold">Pickup Hub</label>
              <select
                value={pickup}
                onChange={(e) => setPickup(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-slate-800 focus:outline-none focus:border-orange-500"
              >
                {locations.map((loc) => (
                  <option key={loc.id} value={loc.id}>
                    {loc.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-slate-700 mb-1 font-bold">Drop Hub</label>
              <select
                value={drop}
                onChange={(e) => setDrop(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-slate-800 focus:outline-none focus:border-orange-500"
              >
                {locations.map((loc) => (
                  <option key={loc.id} value={loc.id}>
                    {loc.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-slate-700 mb-1 font-bold">Weight (kg)</label>
              <input
                type="number"
                step="0.1"
                value={weightKg}
                onChange={(e) => setWeightKg(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-slate-800 font-mono focus:outline-none focus:border-orange-500 font-semibold"
                required
              />
            </div>

            <div>
              <label className="block text-slate-700 mb-1 font-bold">Profit (₹)</label>
              <input
                type="number"
                step="1"
                value={profit}
                onChange={(e) => setProfit(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-emerald-700 font-mono focus:outline-none focus:border-orange-500 font-bold"
                required
              />
            </div>

            <div>
              <label className="block text-slate-700 mb-1 font-bold">Deadline (m)</label>
              <input
                type="number"
                value={deadlineMinutes}
                onChange={(e) => setDeadlineMinutes(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-orange-600 font-mono focus:outline-none focus:border-orange-500 font-bold"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-slate-700 mb-1 font-bold">Package Name</label>
              <input
                type="text"
                value={packageType}
                onChange={(e) => setPackageType(e.target.value)}
                placeholder="e.g. Hardware"
                className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-slate-800 focus:outline-none focus:border-orange-500"
              />
            </div>

            <div>
              <label className="block text-slate-700 mb-1 font-bold">Priority</label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as any)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-slate-800 focus:outline-none focus:border-orange-500 font-semibold"
              >
                <option value="HIGH">HIGH (Urgent)</option>
                <option value="MEDIUM">MEDIUM (Standard)</option>
                <option value="LOW">LOW (Economy)</option>
              </select>
            </div>
          </div>

          <div className="pt-4 flex items-center justify-end gap-2 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-bold transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-lg shadow-md shadow-orange-500/20 transition-colors"
            >
              Confirm & Add
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
