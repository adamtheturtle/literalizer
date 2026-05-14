module Main

type Val =
    | FFloat of float
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FFloat(-0.0);
        FFloat 1.5
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FFloat(-0.0);
        FFloat 1.5
    ]
    ignore my_data
