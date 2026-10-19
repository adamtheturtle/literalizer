struct Record1 { let x: String }
struct Record2 { let x: Int }
struct Record0 { let direct: Record1; let bound: Record2 }
let first = Record2(
    x: 1,
)
let my_data = Record0(
    direct: Record1(
        x: "s",
    ),
    bound: first,
)
