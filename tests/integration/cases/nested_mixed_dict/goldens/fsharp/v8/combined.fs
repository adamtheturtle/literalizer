module Main

type Val =
    | FNull
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("outer", FMap [("a", FInt 1L); ("b", FStr "x"); ("c", FNull)])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("outer", FMap [("a", FInt 1L); ("b", FStr "x"); ("c", FNull)])
    ]
    ignore my_data
