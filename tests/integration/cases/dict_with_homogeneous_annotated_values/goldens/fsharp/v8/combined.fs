module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("a", FList []);
        ("b", FList [])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("a", FList []);
        ("b", FList [])
    ]
    ignore my_data
