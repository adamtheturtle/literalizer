module Main

type Val =
    | FInt of int64
// after
let private _mainDeclaration () =
    let mutable my_data: Val = FInt 42L
    ignore my_data

let private _mainAssignment () =
    // after
    let my_data: Val = FInt 42L
    ignore my_data
