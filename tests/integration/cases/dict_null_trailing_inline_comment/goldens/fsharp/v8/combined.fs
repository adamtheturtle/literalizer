module Main

type Val =
    | FNull
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("host", FStr "localhost");
        ("port", FNull)  // not configured yet
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("host", FStr "localhost");
        ("port", FNull)  // not configured yet
    ]
    ignore my_data
