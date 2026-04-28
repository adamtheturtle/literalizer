module Main

type Val =
    | FInt of bigint
let private _mainDeclaration () =
    let mutable my_data: Val = FInt 9223372036854775808I
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FInt 9223372036854775808I
    ignore my_data
