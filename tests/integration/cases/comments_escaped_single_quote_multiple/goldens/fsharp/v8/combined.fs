module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("host", FStr "it's here");  // a comment
        ("port", FInt 80L)  // another
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("host", FStr "it's here");  // a comment
        ("port", FInt 80L)  // another
    ]
    ignore my_data
