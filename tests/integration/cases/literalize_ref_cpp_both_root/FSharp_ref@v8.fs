module Main

type Val =
    | FInt of int64
    | FList of Val list
let private _mainDeclaration () =
    let mutable shared: Val = FList [
        FInt 1L;
        FInt 2L
    ]
    let mutable my_data: Val = shared
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = shared
    ignore my_data
