module Main

type Val =
    | FList of Val list
    | FDate of System.DateOnly
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FDate (System.DateOnly(2024, 1, 15));
        FDate (System.DateOnly(2024, 2, 20))
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FDate (System.DateOnly(2024, 1, 15));
        FDate (System.DateOnly(2024, 2, 20))
    ]
    ignore my_data
