module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
    | FInt of int64
let my_data: Val = FMap [
    ("positive", [|FMap [("item", [|FInt 2147483648L|])]|]);
    ("negative", [|FMap [("item", [|FInt(-2147483649L)|])]|]);
    ("mixed", [|FMap [("item", [|FInt 0L; FInt 2147483648L|])]|])
]
