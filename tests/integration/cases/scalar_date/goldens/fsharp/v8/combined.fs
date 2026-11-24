module Main

type Val =
    | FDate of System.DateOnly
let private _mainDeclaration () =
    let mutable my_data: Val = FDate (System.DateOnly(2024, 1, 15))
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FDate (System.DateOnly(2024, 1, 15))
    ignore my_data
