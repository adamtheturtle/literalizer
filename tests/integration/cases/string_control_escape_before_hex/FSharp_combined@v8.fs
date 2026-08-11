module Main

type Val =
    | FStr of string
let private _mainDeclaration () =
    let mutable my_data: Val = FStr "aface"
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FStr "aface"
    ignore my_data
