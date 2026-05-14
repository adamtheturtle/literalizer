module Main

type Val =
    | FStr of string
    | FDate of System.DateTime
let private _mainDeclaration () =
    let mutable my_data: Val = FStr (string (System.DateOnly(2024, 1, 15)))
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FStr (string (System.DateOnly(2024, 1, 15)))
    ignore my_data
