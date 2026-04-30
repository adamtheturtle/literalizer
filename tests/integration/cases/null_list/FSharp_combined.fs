module Main

type Val =
    | FNull
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FNull;
        FNull
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FNull;
        FNull
    ]
    ignore my_data
