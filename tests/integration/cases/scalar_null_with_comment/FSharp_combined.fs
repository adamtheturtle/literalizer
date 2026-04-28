module Main

type Val =
    | FNull
// note
let private _mainDeclaration () =
    let mutable my_data: Val = FNull
    ignore my_data

let private _mainAssignment () =
    // note
    let my_data: Val = FNull
    ignore my_data
