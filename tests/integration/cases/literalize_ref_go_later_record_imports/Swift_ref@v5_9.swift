import Foundation
struct Record1 { let x: Int }
struct Record2 { let day: Date; let stamp: Date }
struct Record0 { let plain: Record1; let timed: Record2 }
let plain = Record1(
    x: 1,
)
let timed = Record2(
    day: DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2001, month: 1, day: 2).date!,
    stamp: DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2001, month: 1, day: 2, hour: 3, minute: 4, second: 5).date!,
)
let my_data = Record0(
    plain: plain,
    timed: timed,
)
