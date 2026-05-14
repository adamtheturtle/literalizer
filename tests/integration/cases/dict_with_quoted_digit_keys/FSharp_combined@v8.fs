module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("0a", FStr "first");
        ("1b", FStr "second")
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("0a", FStr "first");
        ("1b", FStr "second")
    ]
    ignore my_data
