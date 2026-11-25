module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("first", FList [
        FInt 1L;
        FInt 2L
    ]);
    ("second", FInt 3L)  // About the second key.
]
