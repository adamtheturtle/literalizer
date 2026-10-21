struct Record1 { let items: [Int] }
struct Record0 { let outer: Record1 }
let recordData = Record1(
    items: [
        1,
        2,
    ],
)
let my_data = Record0(
    outer: recordData,
)
