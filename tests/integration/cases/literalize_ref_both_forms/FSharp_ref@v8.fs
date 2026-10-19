module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable sharedValues: Val = FList [
        FInt 1L;
        FInt 2L
    ]
    let mutable my_data: Val = FMap [
        ("a", sharedValues)
    ]
    ignore my_data

let private _mainAssignment () =
    let mutable sharedValues: Val = FList [
        FInt 1L;
        FInt 2L
    ]
    let mutable my_data: Val = FMap [
        ("a", sharedValues)
    ]
    let my_data: Val = FMap [
        ("a", sharedValues)
    ]
    ignore my_data
