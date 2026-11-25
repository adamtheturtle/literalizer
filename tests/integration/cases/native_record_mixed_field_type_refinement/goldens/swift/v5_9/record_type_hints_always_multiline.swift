struct Record2 { let value: Int }
struct Record1 { let items: [Any] }
struct Record4 { let value: String }
struct Record3 { let items: [Any] }
struct Record0 { let first: Record1; let second: Record3 }
let my_data: Record0 = Record0(
    first: Record1(
        items: [
            1,
            Record2(
                value: 2,
            ),
        ],
    ),
    second: Record3(
        items: [
            1,
            Record4(
                value: "s",
            ),
        ],
    ),
)
