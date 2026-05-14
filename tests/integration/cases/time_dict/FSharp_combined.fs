open System
module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("morning", TimeOnly(9, 30, 0));
        ("afternoon", TimeOnly(14, 15, 0));
        ("evening", TimeOnly(23, 59, 59))
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("morning", TimeOnly(9, 30, 0));
        ("afternoon", TimeOnly(14, 15, 0));
        ("evening", TimeOnly(23, 59, 59))
    ]
    ignore my_data
