module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FSet of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FSet [
        FFloat 2.5;
        FInt 1L
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FSet [
        FFloat 2.5;
        FInt 1L
    ]
    ignore my_data
