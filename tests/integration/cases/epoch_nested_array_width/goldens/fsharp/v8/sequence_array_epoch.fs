module Main

type Val =
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
    | FInt of int64
let my_data: Val = FMap [
    ("positive", FList ([|FMap [("item", FList ([|FInt 2147483648L|]))]|]));
    ("negative", FList ([|FMap [("item", FList ([|FInt(-2147483649L)|]))]|]));
    ("mixed", FList ([|FMap [("item", FList ([|FInt 0L; FInt 2147483648L|]))]|]))
]
