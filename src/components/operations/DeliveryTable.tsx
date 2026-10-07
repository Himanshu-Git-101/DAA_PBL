import React, { useState, useMemo } from 'react';
import { DeliveryRequest } from '../../types';
import { Search, ArrowUpDown, Plus, Filter, AlertCircle, CheckCircle2, Clock } from 'lucide-react';

interface DeliveryTableProps {
  deliveries: DeliveryRequest[];
  selectedDeliveryId: string | null;
  onSelectDeliveryId: (id: string | null) => void;
  onOpenAddModal: () => void;
}

type SortField = "id" | "deadlineMinutesFromStart" | "profit" | "weightKg" | "status" | "pickupLocationId" | "dropLocationId";
type SortOrder = "asc" | "desc";

export const DeliveryTable: React.FC<DeliveryTableProps> = ({
  deliveries,
  selectedDeliveryId,
  onSelectDeliveryId,
  onOpenAddModal
}) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [sortField, setSortField] = useState<SortField>("deadlineMinutesFromStart");
  const [sortOrder, setSortOrder] = useState<SortOrder>("asc");

  const filteredDeliveries = useMemo(() => {
    return deliveries
      .filter(d => {
        const matchesSearch =
          d.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
          d.pickupLocationId.toLowerCase().includes(searchTerm.toLowerCase()) ||
          d.dropLocationId.toLowerCase().includes(searchTerm.toLowerCase()) ||
          d.packageType.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesStatus = statusFilter === "all" || d.status === statusFilter;

        return matchesSearch && matchesStatus;
      })
      .sort((a, b) => {
        let valA: any = a[sortField];
        let valB: any = b[sortField];

        if (typeof valA === "string") {
          valA = valA.toLowerCase();
          valB = valB.toLowerCase();
        }

        if (valA < valB) return sortOrder === "asc" ? -1 : 1;
        if (valA > valB) return sortOrder === "asc" ? 1 : -1;
        return 0;
      });
  }, [deliveries, searchTerm, statusFilter, sortField, sortOrder]);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortOrder("asc");
    }
  };

  return (
    <div className="delivery-table-container flex flex-col h-full bg-white rounded-xl overflow-hidden text-xs">
      {/* Header & Filter Controls */}
      <div className="p-3 border-b border-orange-100 bg-white flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <span className="font-bold text-slate-900 text-xs">Orders List</span>
          <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-orange-100 text-orange-700">
            {deliveries.length}
          </span>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          {/* Search Input */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search ID, location..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-orange-500 w-40 sm:w-48 transition-colors"
            />
          </div>

          {/* Status Filter */}
          <div className="flex items-center gap-1 bg-slate-50 border border-slate-200 rounded-lg px-2 py-1 text-xs text-slate-600">
            <Filter className="w-3 h-3 text-slate-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-transparent border-none text-xs text-slate-700 font-medium focus:outline-none cursor-pointer"
            >
              <option value="all">All Status</option>
              <option value="pending">Pending</option>
              <option value="selected">Selected (Route)</option>
              <option value="deferred">Deferred</option>
            </select>
          </div>

          {/* Add Delivery Button */}
          <button
            onClick={onOpenAddModal}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-orange-500 hover:bg-orange-600 text-white text-xs font-bold rounded-lg shadow-sm transition-all active:scale-95"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Delivery</span>
          </button>
        </div>
      </div>

      {/* Table Content */}
      <div className="flex-1 overflow-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead className="sticky top-0 bg-orange-50/70 border-b border-orange-100 z-10 text-slate-700 font-bold select-none">
            <tr>
              <th
                onClick={() => handleSort("id")}
                className="py-2.5 px-3 cursor-pointer hover:text-orange-600 transition-colors"
              >
                <div className="flex items-center gap-1">
                  <span>ID</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort("status")}
                className="py-2.5 px-3 cursor-pointer hover:text-orange-600 transition-colors"
              >
                <div className="flex items-center gap-1">
                  <span>Status</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort("pickupLocationId")}
                className="py-2.5 px-3 cursor-pointer hover:text-orange-600 transition-colors"
              >
                <div className="flex items-center gap-1">
                  <span>Pickup → Drop</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort("weightKg")}
                className="py-2.5 px-3 cursor-pointer hover:text-orange-600 transition-colors text-right"
              >
                <div className="flex items-center justify-end gap-1">
                  <span>Weight</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort("profit")}
                className="py-2.5 px-3 cursor-pointer hover:text-orange-600 transition-colors text-right"
              >
                <div className="flex items-center justify-end gap-1">
                  <span>Profit</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
              <th
                onClick={() => handleSort("deadlineMinutesFromStart")}
                className="py-2.5 px-3 cursor-pointer hover:text-orange-600 transition-colors text-right"
              >
                <div className="flex items-center justify-end gap-1">
                  <span>Deadline</span>
                  <ArrowUpDown className="w-3 h-3" />
                </div>
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100">
            {filteredDeliveries.length === 0 ? (
              <tr>
                <td colSpan={6} className="py-12 text-center text-slate-400">
                  <div className="flex flex-col items-center justify-center gap-2">
                    <AlertCircle className="w-6 h-6 text-slate-300" />
                    <span>No delivery requests match the current filters.</span>
                  </div>
                </td>
              </tr>
            ) : (
              filteredDeliveries.map((d) => {
                const isSelected = d.id === selectedDeliveryId;

                let statusBadge = (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-slate-100 text-slate-700 border border-slate-200">
                    <Clock className="w-2.5 h-2.5" /> Pending
                  </span>
                );

                if (d.status === "selected") {
                  statusBadge = (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      <CheckCircle2 className="w-2.5 h-2.5" /> In Route
                    </span>
                  );
                } else if (d.status === "deferred") {
                  statusBadge = (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-rose-50 text-rose-700 border border-rose-200" title={d.deferredReason}>
                      <AlertCircle className="w-2.5 h-2.5" /> Deferred
                    </span>
                  );
                }

                return (
                  <tr
                    key={d.id}
                    onClick={() => onSelectDeliveryId(isSelected ? null : d.id)}
                    className={`cursor-pointer transition-colors ${
                      isSelected
                        ? "bg-orange-50/80 border-l-4 border-l-orange-500 font-semibold"
                        : "hover:bg-orange-50/30"
                    }`}
                  >
                    <td className="py-2.5 px-3 font-mono font-bold text-slate-800">
                      {d.id}
                    </td>
                    <td className="py-2.5 px-3">
                      {statusBadge}
                    </td>
                    <td className="py-2.5 px-3 text-slate-700">
                      <div className="flex items-center gap-1.5">
                        <span className="font-bold text-slate-900">{d.pickupLocationId}</span>
                        <span className="text-orange-500 font-bold">→</span>
                        <span className="font-bold text-slate-900">{d.dropLocationId}</span>
                      </div>
                      <div className="text-[11px] text-slate-500 truncate max-w-[160px]">
                        {d.packageType}
                      </div>
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono text-slate-700">
                      {d.weightKg.toFixed(1)} kg
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono text-emerald-600 font-bold">
                      ₹{d.profit}
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono text-orange-600 font-bold">
                      {d.deadlineMinutesFromStart}m
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
