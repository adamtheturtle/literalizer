module Main

type Val =
    | FInt of int64
let private _mainDeclaration () =
    let mutable my_data: Val = FInt 2147483648L
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FInt 2147483648L
    ignore my_data
