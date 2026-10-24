import Foundation
let my_data: [String: Any] = [
    "date": "0099-05-27",
    "naive": Date(timeIntervalSince1970: -62135551800.0),
    "recent": DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2024, month: 5, day: 27, hour: 10, minute: 0, second: 0).date!,
]
