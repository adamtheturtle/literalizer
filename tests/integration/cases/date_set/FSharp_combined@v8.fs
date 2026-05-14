module Main

type Val =
    | FSet of Val list
    | FStr of string
    | FDate of System.DateTime
let private _mainDeclaration () =
    let mutable my_data: Val = FSet [
        FStr (string (System.DateOnly(2024, 1, 15)));
        FStr (string (System.DateOnly(2024, 6, 1)))
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FSet [
        FStr (string (System.DateOnly(2024, 1, 15)));
        FStr (string (System.DateOnly(2024, 6, 1)))
    ]
    ignore my_data
