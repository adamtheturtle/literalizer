module Main

type Val =
    | FFloat of float
let private _mainDeclaration () =
    let mutable my_data: Val = FFloat 3.14
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FFloat 3.14
    ignore my_data
