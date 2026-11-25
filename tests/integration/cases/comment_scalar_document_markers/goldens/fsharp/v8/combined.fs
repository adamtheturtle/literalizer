module Main

type Val =
    | FInt of int64
// note
let private _mainDeclaration () =
    let mutable my_data: Val = FInt 42L
    ignore my_data

let private _mainAssignment () =
    // note
    let my_data: Val = FInt 42L
    ignore my_data
