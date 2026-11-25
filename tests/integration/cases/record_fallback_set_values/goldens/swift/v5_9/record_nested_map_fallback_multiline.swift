struct Record0 { let name: String; let payload: [String: Any?] }
let my_data = [
    Record0(
        name: "one",
        payload: [
            "scalar": 1,
            "items": Set<AnyHashable>([
                2,
                3,
            ]),
        ],
    ),
    Record0(
        name: "two",
        payload: [
            "other": 2,
        ],
    ),
]
