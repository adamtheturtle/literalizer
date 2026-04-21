module Check

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        ("a", FInt 1L);
        ("b", FStr "x")
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        ("a", FInt 1L);
        ("b", FStr "x")
    ]
    ignore my_data
