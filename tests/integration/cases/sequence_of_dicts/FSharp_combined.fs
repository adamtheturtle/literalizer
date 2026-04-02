module Check

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let mutable my_data: Val = FList [
    FMap [("name", FStr "Alice"); ("age", FInt 30L)];
    FMap [("name", FStr "Bob"); ("age", FInt 25L)]
]
