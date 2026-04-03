module Check

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        ("name", FStr "Alice");
        ("scores", FList [FInt 10L; FInt 20L; FInt 30L])
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        ("name", FStr "Alice");
        ("scores", FList [FInt 10L; FInt 20L; FInt 30L])
    ]
    ignore my_data
