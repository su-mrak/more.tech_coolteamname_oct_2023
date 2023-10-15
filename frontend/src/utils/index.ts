import {Schedule, WeekSchedule} from "./backend"

import _ from "lodash"

export * from "./colors"
export * from "./hooks"
export * from "./styles"

export function formatDistance(distance: number | null): string {
  if (distance === null) {
    return ""
  }

  return distance < 1000 ?
    `${distance.toFixed(0)} м` :
    `${(distance / 1000).toFixed(1)} км`
}

export function reduceSchedule(schedule: WeekSchedule) {
  const daysOrder = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
  const ruDays = {
    monday: "пн",
    tuesday: "вт",
    wednesday: "ср",
    thursday: "чт",
    friday: "пт",
    saturday: "сб",
    sunday: "вс",
  }

  const result: {start: string, end: string | null, schedule: Schedule | null}[] = []
  for (const day of daysOrder) {
    const current = schedule[day] || null
    if (result.length === 0 || !_.isEqual(result[result.length - 1].schedule, current)) {
      result.push({start: ruDays[day], end: null, schedule: current || null})
    } else {
      result[result.length - 1].end = ruDays[day]
    }
  }

  return result.map(
    v => {
      const delta = `${v.start}${v.end !== null ? "-" + v.end : ""}`
      let workingHours;
      if (v.schedule === null) {
        workingHours = "выходной"
      } else if (v.schedule.breakStartsAt && v.schedule.breakEndsAt) {
        workingHours = [
          `${v.schedule.opensAt.slice(0, -3)}-${v.schedule.breakStartsAt.slice(0, -3)}`,
          `${v.schedule.breakEndsAt.slice(0, -3)}-${v.schedule.closesAt.slice(0, -3)}`
        ].join(", ")
      } else {
        workingHours = `${v.schedule.opensAt.slice(0, -3)}-${v.schedule.closesAt.slice(0, -3)}`
      }
      return `${delta}: ${workingHours}`
    }
  )
}
