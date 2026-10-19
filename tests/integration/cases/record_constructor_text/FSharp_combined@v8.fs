module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("text", FStr "Record0(");
        ("number", FInt 1L)
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("text", FStr "Record0(");
        ("number", FInt 1L)
    ]
    ignore my_data
