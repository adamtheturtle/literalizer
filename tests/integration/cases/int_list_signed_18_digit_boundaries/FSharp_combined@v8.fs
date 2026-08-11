module Main

type Val =
    | FInt of int64
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FInt 999999999999999999L;
        FInt(-999999999999999999L)
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FInt 999999999999999999L;
        FInt(-999999999999999999L)
    ]
    ignore my_data
