module Check

let process (_a: obj, _b: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
let items: Val = FList [
process(1, 42),
process(2, 100)
]
