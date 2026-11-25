struct Record1 { let kind: String; let urgent: Bool }
struct Record0 { let entries: [Record1] }
struct Record3 { let error: String }
struct Record2 { let entries: [Record3] }
let my_data: [String: Any] = [
    "left": Record0(
        entries: [
            Record1(
                kind: "add",
                urgent: true,
            ),
        ],
    ),
    "right": Record2(
        entries: [
            Record3(
                error: "not_found",
            ),
        ],
    ),
]
