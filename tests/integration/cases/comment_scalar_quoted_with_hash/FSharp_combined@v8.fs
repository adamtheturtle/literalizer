module Main

type Val =
    | FStr of string
// note
let private _mainDeclaration () =
    let mutable my_data: Val = FStr "hello # world"
    ignore my_data

let private _mainAssignment () =
    // note
    let my_data: Val = FStr "hello # world"
    ignore my_data
