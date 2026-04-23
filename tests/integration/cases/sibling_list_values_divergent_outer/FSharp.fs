module Check

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FList [FInt 1L]);
    ("b", FList [FStr "x"])
]
