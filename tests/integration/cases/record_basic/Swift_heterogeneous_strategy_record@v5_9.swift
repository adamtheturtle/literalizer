struct Record0 { let id: Int; let label: String; let enabled: Bool; let related_ids: [Int] }
let my_data: Any = Record0(
    id: 1,
    label: "She said \"hello\", then waved",
    enabled: false,
    related_ids: [
        1,
        2,
        3,
    ],
)
