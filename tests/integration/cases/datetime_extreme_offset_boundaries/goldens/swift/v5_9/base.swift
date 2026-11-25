import Foundation
let my_data = [
    DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2020, month: 6, day: 16, hour: 11, minute: 59, second: 0).date!,
    DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: -64800)!, year: 2020, month: 6, day: 15, hour: 12, minute: 0, second: 0).date!,
    DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 64800)!, year: 2020, month: 6, day: 15, hour: 12, minute: 0, second: 0).date!,
    DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2020, month: 6, day: 14, hour: 12, minute: 1, second: 0).date!,
]
