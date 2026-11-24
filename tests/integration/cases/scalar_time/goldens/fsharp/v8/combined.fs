module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("starts_at", FStr (string (System.TimeOnly(9, 30, 0))))
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("starts_at", FStr (string (System.TimeOnly(9, 30, 0))))
    ]
    ignore my_data
