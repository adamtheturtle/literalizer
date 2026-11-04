struct Record1 { let pair: [Any] }
struct Record0 { let outer: Record1 }
let my_data: [Record0] = [
    Record0(
        outer: Record1(
            pair: [
                1,
                "first",
            ],
        ),
    ),
    Record0(
        outer: Record1(
            pair: [
                false,
                "second",
            ],
        ),
    ),
]
