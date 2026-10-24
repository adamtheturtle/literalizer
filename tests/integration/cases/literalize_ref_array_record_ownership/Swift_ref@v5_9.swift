struct Record1 { let values: [Int] }
struct Record2 { let nested: [[Int]] }
struct Record0 { let trivial: Record1; let nested: Record2 }
let trivial = Record1(
    values: [
        1,
        2,
    ],
)
let nested = Record2(
    nested: [
        [
            1,
            2,
        ],
        [
            3,
            4,
        ],
    ],
)
let my_data = Record0(
    trivial: trivial,
    nested: nested,
)
