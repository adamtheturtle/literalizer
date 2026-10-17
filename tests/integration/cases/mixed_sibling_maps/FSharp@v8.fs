module Main

type Val =
    | FNull
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FList [FMap [("a", FInt 1L)]; FMap [("a", FNull)]; FInt 42L];
    FList [FMap [("a", FInt 1L)]; FMap [("a", FStr "s")]; FInt 42L];
    FList [FMap [("a", FInt 1L)]; FMap [("a", FNull)]];
    FList [FMap [("a", FInt 1L)]; FMap [("a", FStr "s")]]
]
