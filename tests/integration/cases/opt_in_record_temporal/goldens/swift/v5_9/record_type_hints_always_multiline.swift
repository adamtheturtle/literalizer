import Foundation
struct Record0 { let event_date: Date; let event_time: String; let event_datetime: Date }
let my_data: Record0 = Record0(
    event_date: DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2024, month: 1, day: 15).date!,
    event_time: "12:30:00",
    event_datetime: DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2024, month: 1, day: 15, hour: 12, minute: 30, second: 0).date!,
)
