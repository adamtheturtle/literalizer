module Main

type Val =
    | FSet of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FSet []
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FSet []
    ignore my_data
