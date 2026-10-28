import Foundation
let my_data: [String: Any] = [
    "before_date": "1582-10-04",
    "gap_date": "1582-10-10",
    "transition_date": "1582-10-15",
    "after_date": "1582-10-16",
    "before_naive": Date(timeIntervalSince1970: -12220198199.999998),
    "gap_naive": Date(timeIntervalSince1970: -12219679799.5),
    "transition_positive": Date(timeIntervalSince1970: -12219355800.0),
    "transition_negative": Date(timeIntervalSince1970: -12219143400.0),
    "after_positive": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 64800)!, year: 1582, month: 10, day: 16, hour: 0, minute: 30, second: 0).date!,
]
