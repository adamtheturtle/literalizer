module Main

type Val =
    | FStr of string
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FStr "48656c6c6f"
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FStr "48656c6c6f"
    ]
    ignore my_data
