module Main

type Val =
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FMap [];
        FMap []
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FMap [];
        FMap []
    ]
    ignore my_data
