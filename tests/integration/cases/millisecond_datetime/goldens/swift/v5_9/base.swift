import Foundation
let my_data = [
    "half": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 1979, month: 5, day: 27, hour: 7, minute: 32, second: 0, nanosecond: 500000000).date!,
    "milli": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 1979, month: 5, day: 27, hour: 7, minute: 32, second: 0, nanosecond: 100000000).date!,
    "max_milli": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 1979, month: 5, day: 27, hour: 7, minute: 32, second: 0, nanosecond: 999000000).date!,
    "whole": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 1979, month: 5, day: 27, hour: 7, minute: 32, second: 0).date!,
]
