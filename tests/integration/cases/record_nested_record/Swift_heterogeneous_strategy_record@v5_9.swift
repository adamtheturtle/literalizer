struct Record1 { let name: String; let age: Int }
struct Record0 { let id: Int; let owner: Record1 }
let my_data: Any = Record0(
    id: 1,
    owner: Record1(
        name: "Alice",
        age: 30,
    ),
)
