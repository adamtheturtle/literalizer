struct Record1 { let a: Int; let b: String; let c: Any? }
struct Record0 { let outer: Record1 }
let my_data: Any = Record0(
    outer: Record1(
        a: 1,
        b: "x",
        c: nil,
    ),
)
