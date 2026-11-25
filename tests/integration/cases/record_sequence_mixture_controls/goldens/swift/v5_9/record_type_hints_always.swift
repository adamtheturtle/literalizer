struct Record0 { let x: Int }
let my_data: [Any] = [
    [[1], Record0(x: 1)],
    [Record0(x: 1), Record0(x: 2)],
    [[], [Record0(x: 1)]],
    [[Any](), [Any]()],
]
