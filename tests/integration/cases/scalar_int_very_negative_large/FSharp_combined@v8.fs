module Main

type Val =
    | FInt of int64
    | FBigInt of bigint
let private _mainDeclaration () =
    let mutable my_data: Val = FBigInt(-9223372036854775809I)
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FBigInt(-9223372036854775809I)
    ignore my_data
