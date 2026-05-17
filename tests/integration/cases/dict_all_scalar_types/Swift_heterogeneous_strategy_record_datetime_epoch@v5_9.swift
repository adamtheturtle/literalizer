import Foundation
struct Record0 { let s: String; let i: Int; let f: Double; let b: Bool; let n: Any?; let d: Date; let dt: Int; let by: String }
let my_data: Any = Record0(
    s: "string",
    i: 1,
    f: 1.5,
    b: true,
    n: nil,
    d: DateComponents(calendar: Calendar(identifier: .gregorian), year: 2024, month: 1, day: 15).date!,
    dt: 1705320000,
    by: "48656c6c6f",
)
