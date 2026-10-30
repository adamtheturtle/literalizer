struct Record1 { let item: Int }
struct Record2 { let item: Any? }
struct Record0 { let integers: [Any]; let nulls: [Any]; let nested: [[Any]]; let reversed: [Any] }
let my_data: Record0 = Record0(
    integers: [
        [],
        [
            Record1(
                item: 1,
            ),
        ],
    ],
    nulls: [
        [],
        [
            Record2(
                item: nil,
            ),
        ],
    ],
    nested: [
        [
            [],
            [
                Record1(
                    item: 2,
                ),
            ],
        ],
        [
            [
                Record1(
                    item: 3,
                ),
            ],
            [],
        ],
    ],
    reversed: [
        [
            Record1(
                item: 4,
            ),
        ],
        [],
    ],
)
