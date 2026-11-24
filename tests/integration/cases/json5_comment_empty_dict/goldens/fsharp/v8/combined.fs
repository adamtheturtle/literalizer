module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    // empty heading
    // empty body
    // after empty
    let mutable my_data: Val = FMap []
    ignore my_data

let private _mainAssignment () =
    // empty heading
    // empty body
    // after empty
    let my_data: Val = FMap []
    ignore my_data
