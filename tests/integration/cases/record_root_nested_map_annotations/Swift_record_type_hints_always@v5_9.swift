struct Record0 { let x: Int }
let my_data: [String: [[String: Record0]]] = [
    "outer": [["inner": Record0(x: 1)], ["inner": Record0(x: 2)]],
]
