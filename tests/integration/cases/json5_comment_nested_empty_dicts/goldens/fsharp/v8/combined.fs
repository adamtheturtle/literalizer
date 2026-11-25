module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        // outer heading
        // first empty
        ("a", FMap []);
        // second empty
        ("b", FMap [])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        // outer heading
        // first empty
        ("a", FMap []);
        // second empty
        ("b", FMap [])
    ]
    ignore my_data
