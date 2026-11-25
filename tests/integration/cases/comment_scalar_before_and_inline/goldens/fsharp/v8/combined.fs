module Main

type Val =
    | FStr of string
// before
// inline
let private _mainDeclaration () =
    let mutable my_data: Val = FStr "plain"
    ignore my_data

let private _mainAssignment () =
    // before
    // inline
    let my_data: Val = FStr "plain"
    ignore my_data
