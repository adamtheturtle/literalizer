import Foundation
struct Record0 { let birthday: Date; let moment: Date; let at: String }
let my_data: Record0 = Record0(
    birthday: DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2024, month: 1, day: 15).date!,
    moment: DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2024, month: 1, day: 15, hour: 12, minute: 30, second: 0).date!,
    at: "09:30:00",
)
