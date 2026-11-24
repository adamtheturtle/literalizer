module Main

type Val =
    | FNull
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        // comment
        ("name", FStr "Alice");
        ("score", FNull)
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        // comment
        ("name", FStr "Alice");
        ("score", FNull)
    ]
    ignore my_data
