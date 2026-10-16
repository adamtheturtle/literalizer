module Main

type Val =
    | FList of Val list
let private _mainDeclaration () =
    // empty heading
    // empty body
    // after empty
    let mutable my_data: Val = FList []
    ignore my_data

let private _mainAssignment () =
    // empty heading
    // empty body
    // after empty
    let my_data: Val = FList []
    ignore my_data
