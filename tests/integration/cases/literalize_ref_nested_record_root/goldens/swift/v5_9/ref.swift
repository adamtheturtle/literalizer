struct Record1 { let value: Int }
struct Record0 { let child: Record1 }
let first = Record0(
    child: Record1(
        value: 1,
    ),
)
let my_data = first
