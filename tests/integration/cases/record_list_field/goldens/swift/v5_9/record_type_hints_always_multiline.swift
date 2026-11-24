struct Record1 { let a: Int }
struct Record0 { let items: [Record1] }
let my_data: Record0 = Record0(
    items: [
        Record1(
            a: 1,
        ),
    ],
)
