module Check

type Val =
    | FNull
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        ("outer", FMap [("a", FInt 1L); ("b", FStr "x"); ("c", FNull)])
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        ("outer", FMap [("a", FInt 1L); ("b", FStr "x"); ("c", FNull)])
    ]
    ignore my_data
