module Main

type Val =
    | FFloat of float
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FFloat infinity;
        FFloat(-infinity);
        FFloat nan
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FFloat infinity;
        FFloat(-infinity);
        FFloat nan
    ]
    ignore my_data
