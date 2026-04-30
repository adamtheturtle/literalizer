module Main

type Val =
    | FStr of string
    | FList of Val list
    | FSet of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FSet [FStr "a"; FStr "b"]
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FSet [FStr "a"; FStr "b"]
    ]
    ignore my_data
