module Main

type Val =
    | FNull
    | FInt of int64
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
let my_data: Val array = [|
    FList ([|FMap [("a", FInt 1L)]; FMap [("a", FNull)]; FInt 42L|]);
    FList ([|FMap [("a", FInt 1L)]; FMap [("a", FStr "s")]; FInt 42L|]);
    FList ([|FMap [("a", FInt 1L)]; FMap [("a", FNull)]|]);
    FList ([|FMap [("a", FInt 1L)]; FMap [("a", FStr "s")]|])
|]
