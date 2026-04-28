module Main

type Val =
    | FInt of int64
    | FSet of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FSet [
        FInt 1L;
        FInt 2L;
        FInt 3L
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FSet [
        FInt 1L;
        FInt 2L;
        FInt 3L
    ]
    ignore my_data
