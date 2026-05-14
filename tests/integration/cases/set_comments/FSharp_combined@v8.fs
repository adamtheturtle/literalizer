module Main

type Val =
    | FStr of string
    | FSet of Val list
let private _mainDeclaration () =
    let mutable my_data: Val = FSet [
        FStr "apple";  // inline comment
        // before banana
        FStr "banana"
        // trailing
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FSet [
        FStr "apple";  // inline comment
        // before banana
        FStr "banana"
        // trailing
    ]
    ignore my_data
