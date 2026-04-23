module Check

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        ("a", FList [FInt 1L]);
        ("b", FList [FStr "x"])
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        ("a", FList [FInt 1L]);
        ("b", FList [FStr "x"])
    ]
    ignore my_data
