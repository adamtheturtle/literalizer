import Foundation
struct Record1 { let integer: Int; let boolean: Bool; let decimal: Double; let null: Any? }
struct Record3 { let integer: Int }
struct Record2 { let child: Record3 }
struct Record4 { let text: String }
struct Record5 { let day: Date; let stamp: Date }
struct Record0 { let trivial: Record1; let nested: Record2; let owning: Record4; let calendar: Record5 }
let trivial = Record1(
    integer: 1,
    boolean: true,
    decimal: 1.5,
    null: nil,
)
let nested = Record2(
    child: Record3(
        integer: 2,
    ),
)
let owning = Record4(
    text: "owned",
)
let calendar = Record5(
    day: DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2001, month: 1, day: 2).date!,
    stamp: DateComponents(calendar: Calendar(identifier: .gregorian), timeZone: TimeZone(secondsFromGMT: 0)!, year: 2001, month: 1, day: 2, hour: 3, minute: 4, second: 5).date!,
)
let my_data = Record0(
    trivial: trivial,
    nested: nested,
    owning: owning,
    calendar: calendar,
)
