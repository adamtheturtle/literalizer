module Check

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FMap [("a", FInt 1L)];
        FStr "hello"
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FMap [("a", FInt 1L)];
        FStr "hello"
    ]
    ignore my_data
