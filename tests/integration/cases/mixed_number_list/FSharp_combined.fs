module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FInt 1L;
        FFloat 2.5;
        FInt 3L
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FInt 1L;
        FFloat 2.5;
        FInt 3L
    ]
    ignore my_data
