module Check

type Val =
    | FInt of int64
    | FList of Val list
let process () : obj = null
process(FList [
    FInt 1L
])
