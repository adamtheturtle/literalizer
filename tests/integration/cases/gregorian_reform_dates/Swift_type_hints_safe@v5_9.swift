import Foundation
let my_data = [
    "before_date": Date(timeIntervalSince1970: -12220243200),
    "gap_date": Date(timeIntervalSince1970: -12219724800),
    "transition_date": Date(timeIntervalSince1970: -12219292800),
    "after_date": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 1582, month: 10, day: 16).date!,
    "before_naive": Date(timeIntervalSince1970: -12220198199.999998),
    "gap_naive": Date(timeIntervalSince1970: -12219679799.5),
    "transition_positive": Date(timeIntervalSince1970: -12219355800.0),
    "transition_negative": Date(timeIntervalSince1970: -12219143400.0),
    "after_positive": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 64800)!, year: 1582, month: 10, day: 16, hour: 0, minute: 30, second: 0).date!,
]
