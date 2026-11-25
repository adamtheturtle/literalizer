module Main

type Val =
    | FInt of int64
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
let private _mainDeclaration () =
    let mutable my_data: Val = FInt 42L
    ignore my_data

let private _mainAssignment () =
    // scalar heading
    // second heading line
    // scalar inline
    // inline continuation
    // scalar trailing
    let my_data: Val = FInt 42L
    ignore my_data
