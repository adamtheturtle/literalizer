module Main

type Val =
    | FSet of Val list
    | FDate of System.DateOnly
let private _mainDeclaration () =
    let mutable my_data: Val = FSet [
        FDate (System.DateOnly(2024, 1, 15));
        FDate (System.DateOnly(2024, 6, 1))
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FSet [
        FDate (System.DateOnly(2024, 1, 15));
        FDate (System.DateOnly(2024, 6, 1))
    ]
    ignore my_data
