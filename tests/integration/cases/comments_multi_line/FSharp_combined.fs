module Main

type Val =
    | FStr of string
    | FList of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        // line 1
        // line 2
        FStr "a"
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        // line 1
        // line 2
        FStr "a"
    ]
    ignore my_data
