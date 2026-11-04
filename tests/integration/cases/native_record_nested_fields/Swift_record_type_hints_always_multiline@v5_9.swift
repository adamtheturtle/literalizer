struct Record1 { let name: String; let active: Bool }
struct Record2 { let name: String; let score: Double }
struct Record0 { let owner: Record1; let members: [Record2] }
let my_data: Record0 = Record0(
    owner: Record1(
        name: "Ada",
        active: false,
    ),
    members: [
        Record2(
            name: "Ada",
            score: 1.5,
        ),
        Record2(
            name: "Bob",
            score: 2.5,
        ),
    ],
)
