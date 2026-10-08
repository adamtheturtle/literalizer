import Foundation
let my_data = [
    "date": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 99, month: 5, day: 27).date!,
    "naive": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 1, month: 1, day: 1, hour: 12, minute: 30, second: 0).date!,
    "recent": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2024, month: 5, day: 27, hour: 10, minute: 0, second: 0).date!,
]
