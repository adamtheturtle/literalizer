module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
    | FDate of System.DateTime
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("vals", FList [FStr (string (System.DateOnly(2024, 1, 15))); FStr (string (System.TimeOnly(9, 30, 0)))])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("vals", FList [FStr (string (System.DateOnly(2024, 1, 15))); FStr (string (System.TimeOnly(9, 30, 0)))])
    ]
    ignore my_data
