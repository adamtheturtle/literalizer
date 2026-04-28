module Main

type Val =
    | FStr of string
    | FDatetime of System.DateTime
let private _mainDeclaration () =
    let mutable my_data: Val = FStr (string (System.DateTime(2024, 1, 15, 12, 30, 0)))
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FStr (string (System.DateTime(2024, 1, 15, 12, 30, 0)))
    ignore my_data
