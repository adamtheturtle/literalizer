module Main

type Val =
    | FNull
let private _mainDeclaration () =
    let mutable my_data: Val = FNull
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FNull
    ignore my_data
