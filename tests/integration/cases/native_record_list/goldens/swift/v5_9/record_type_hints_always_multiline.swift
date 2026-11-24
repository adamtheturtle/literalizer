struct Record1 { let age: Int }
struct Record0 { let name: String; let active: Bool; let count: Int; let score: Double; let missing: Any?; let scores: [Int]; let child: Record1 }
let my_data: [Record0] = [
    Record0(
        name: "Ada",
        active: true,
        count: 1,
        score: 1.5,
        missing: nil,
        scores: [
            1,
            2,
        ],
        child: Record1(
            age: 3,
        ),
    ),
    Record0(
        name: "Bob",
        active: false,
        count: 2,
        score: 2.5,
        missing: nil,
        scores: [
            4,
        ],
        child: Record1(
            age: 5,
        ),
    ),
]
