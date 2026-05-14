module Main

type Val =
    | FBool of bool
let private _mainDeclaration () =
    let mutable my_data: Val = FBool true
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FBool true
    ignore my_data
