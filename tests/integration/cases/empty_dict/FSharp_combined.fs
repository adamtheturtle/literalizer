module Main

type Val =
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap []
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap []
    ignore my_data
