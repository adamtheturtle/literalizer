module Check

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let mutable my_data: Val = FList [
    FInt 1L;
    FStr "hello"
]
