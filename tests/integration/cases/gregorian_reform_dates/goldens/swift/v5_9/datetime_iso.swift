import Foundation
let my_data: [String: Any] = [
    "ancient_date": Date(timeIntervalSince1970: -14826672000),
    "modern_date": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2024, month: 1, day: 15).date!,
    "before_date": Date(timeIntervalSince1970: -12220243200),
    "gap_date": Date(timeIntervalSince1970: -12219724800),
    "transition_date": Date(timeIntervalSince1970: -12219292800),
    "after_date": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 1582, month: 10, day: 16).date!,
    "before_naive": "1582-10-04T12:30:00.000001",
    "gap_naive": "1582-10-10T12:30:00.500000",
    "transition_positive": "1582-10-15T00:30:00+18:00",
    "transition_negative": "1582-10-15T23:30:00-18:00",
    "after_positive": "1582-10-16T00:30:00+18:00",
]
