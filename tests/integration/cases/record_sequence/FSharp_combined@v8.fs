module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FMap [("id", FInt 1L); ("label", FStr "first")];
        FMap [("id", FInt 2L); ("label", FStr "second")];
        FMap [("id", FInt 3L); ("label", FStr "third")]
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FMap [("id", FInt 1L); ("label", FStr "first")];
        FMap [("id", FInt 2L); ("label", FStr "second")];
        FMap [("id", FInt 3L); ("label", FStr "third")]
    ]
    ignore my_data
