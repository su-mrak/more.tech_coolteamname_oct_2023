import {FeatureCollection} from "geojson"

export interface Schedule {
  opensAt: string,
  closesAt: string,
  breakStartsAt?: string,
  breakEndsAt?: string,
}

export interface WeekSchedule {
  sunday?: Schedule,
  monday?: Schedule,
  tuesday?: Schedule,
  wednesday?: Schedule,
  thursday?: Schedule,
  friday?: Schedule,
  saturday?: Schedule,
}

export interface Office {
  id: string
  address: string
  coordinate: {lat: number, lng: number}
  salePointName: string
  individualSchedule: WeekSchedule,
  individualIsWorkingNow?: boolean,
  legalEntitySchedule: WeekSchedule,
  legalEntityIsWorkingNow?: boolean,
  metroStation?: string,
  salePointFormat: string,
  officeType: string,
  features: OfficeFeature[],
  durationWalk?: number,
  durationCar?: number,
  load?: number,
  closestMetro?: {
    distance: number,
    name: number,
    line: number,
  }
}

export interface Atm {
  id: string,
  address: string,
  coordinate: {lat: number, lng: number},
  durationWalk?: number,
  durationCar?: number,
  features: AtmFeature[],
  load?: number,
  closestMetro?: {
    distance: number,
    name: number,
    line: number,
  }
}

export type AtmFeature = "BLIND" | "NFC_FOR_BANK_CARDS" | "QR_READ"
  | "SUPPORT_CHARGE_RUB" | "WHEELCHAIR" | "WITHDRAWAL_EUR"
  | "REPLENISHMENT_EUR" | "WITHDRAWAL_RUB" | "REPLENISHMENT_RUB"
  | "WITHDRAWAL_USD" | "REPLENISHMENT_USD"


export type OfficeFeature = "INDIVIDUAL_MORTGAGE_LENDING"
  | "INDIVIDUAL_DEPOSITS"
  | "INDIVIDUAL_CURRENCY_EXCHANGE_OPERATIONS"
  | "LEGAL_ENTITY_LENDING"
  | "LEGAL_ENTITY_SETTLEMENT_SERVICE"
  | "HAS_RAMP"
  | "IS_WORKING_NOW"

interface TopTellerFiltered {
  atms: Atm[],
  offices: Office[]
}

const BACKEND_URL = "https://kodiki-hack.ru:8000"

export async function getOffices(): Promise<Office[]> {
  const request = await fetch(
    `${BACKEND_URL}/offices`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  )
  return await request.json()
}

export async function getAtms(): Promise<Atm[]> {
  const request = await fetch(
    `${BACKEND_URL}/atms`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  )
  return await request.json()
}


export async function getRoutesByTeller(
  start: [number, number], tellerId: string, tellerType: "atm" | "office",
  profile: "foot-walking" | "driving-car"
): Promise<FeatureCollection> {
  const request = await fetch(
    `${BACKEND_URL}/routes/by-teller`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        start: {lng: start[0], lat: start[1]},
        profile,
        tellerId,
        tellerType: tellerType.toUpperCase(),
      })
    }
  )
  return await request.json()
}

export async function getTopTellerFiltered(
  userCoords: [number, number],
  atmFeature: AtmFeature[],
  officeFeature: OfficeFeature[],
  individualIsWorkingNow?: boolean,
  legalEntityIsWorkingNow?: boolean,
): Promise<TopTellerFiltered> {
  const request = await fetch(
    `${BACKEND_URL}/tellers`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        limit: 100,
        lng: userCoords[0],
        lat: userCoords[1],
        atmFeature,
        officeFeature,
        individualIsWorkingNow,
        legalEntityIsWorkingNow,
      })
    }
  )
  return await request.json()
}

export async function confirmTap(tellerId: string, tellerType: "atm" | "office"): Promise<void> {
  await fetch(
    `${BACKEND_URL}/tap?tellerId=${tellerId}&tellerType=${tellerType}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    }
  )
}
