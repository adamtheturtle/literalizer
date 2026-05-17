struct Record1 { let id: Int; let label: String }
struct Record0 { let name: String; let items: [Record1] }
let my_data: Any = Record0(
    name: "box",
    items: [
        Record1(
            id: 1,
            label: "first",
        ),
        Record1(
            id: 2,
            label: "second",
        ),
    ],
)
