struct Record0 { let name: String; let payload: [String: Any?] }
let my_data: [Record0] = [
    Record0(
        name: "one",
        payload: [
            "scalar": 1,
            "empty": Set<AnyHashable>(),
            "mixed": Set<AnyHashable>([
                2,
                "word",
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
