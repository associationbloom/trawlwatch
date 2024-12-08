import { useMemo, useState } from "react"
import { EyeIcon, XIcon } from "lucide-react"

import { Vessel } from "@/types/vessel"
import SidebarExpander from "@/components/ui/custom/sidebar-expander"
import { useMapStore } from "@/libs/stores/map-store"

import TrackedVesselDetails from "./tracked-vessel-details"
import { useShallow } from "zustand/react/shallow"
import { useTrackModeOptionsStore } from "@/libs/stores/track-mode-options-store"

const shipColorsBackground = [
  "bg-vessel-color-1",
  "bg-vessel-color-2",
  "bg-vessel-color-3",
  "bg-vessel-color-4",
  "bg-vessel-color-5",
  "bg-vessel-color-6",
  "bg-vessel-color-7",
  "bg-vessel-color-8",
  "bg-vessel-color-9",
  "bg-vessel-color-10",
  "bg-vessel-color-11",
  "bg-vessel-color-12",
]

export interface TrackedVesselItemProps {
  colorIndex: number
  vessel: Vessel
  className?: string
}

export default function TrackedVesselItem({
  vessel,
  colorIndex = 0,
  className,
}: TrackedVesselItemProps) {
  const { mode: mapMode } = useMapStore(useShallow((state) => ({
    mode: state.mode,
  })))

  const { removeTrackedVessel, vesselsIDsHidden, setVesselVisibility } = useTrackModeOptionsStore(useShallow((state) => ({
    removeTrackedVessel: state.removeTrackedVessel,
    vesselsIDsHidden: state.vesselsIDsHidden,
    setVesselVisibility: state.setVesselVisibility,
  })))

  const isHidden = vesselsIDsHidden.includes(vessel.id)

  const vesselBgColorClass = shipColorsBackground[colorIndex];
  const isTrackMode = mapMode === "track"

  const onRemove = () => {
    removeTrackedVessel(vessel.id)
  }

  const onShowSidebarExpander = () => {
    if (!vessel.excursions_timeframe) {
      return
    }
    setVesselVisibility(vessel.id, !isHidden)
  }

  return (
    <div className="flex gap-1">
      <div className={`flex w-full flex-col gap-2 py-2 ${className}`}>
        <SidebarExpander.Root disabled={!isTrackMode}>
          <SidebarExpander.Header className="flex items-center justify-between">
            <div className="flex w-full flex-col gap-1">
              <div className="flex items-center gap-2">
                {isTrackMode && (
                  <div
                    className={`rounded-full ${vesselBgColorClass} size-4`}
                  ></div>
                )}
                <h6 className="text-sm font-bold">{vessel.ship_name}</h6>
              </div>
              <div>
                <p className="text-sm text-color-4">
                  IMO {vessel.imo} / MMSI {vessel.mmsi} / {vessel.length}m
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={onRemove}
                className="transition-colors hover:text-color-1 hover:text-color-1/40"
              >
                <XIcon className="size-4" />
              </button>
              {isTrackMode && (
                <button
                  onClick={onShowSidebarExpander}
                  className={`transition-colors hover:text-color-1 hover:text-color-1/40 ${!isHidden ? 'text-color-1' : ''}`}
                >
                  <EyeIcon className="size-4" />
                </button>
              )}
            </div>
          </SidebarExpander.Header>
          <SidebarExpander.Content>
            <div className="flex w-full  flex-col">
              <TrackedVesselDetails
                vessel={vessel}
                onExcursionView={() => {}}
                onExcursionFocus={() => {}}
              />
            </div>
          </SidebarExpander.Content>
        </SidebarExpander.Root>
      </div>
    </div>
  )
}
