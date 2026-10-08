module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
    let shared: Val = FList [
        FInt 1L;
        FInt 2L
    ]
    let my_data: Val = FMap [
        ("a", shared)
    ]
