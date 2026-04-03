module Check

type Val =
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FMap [("x", FInt 1L); ("y", FFloat 2.5)];
        FMap [("x", FInt 3L); ("y", FFloat 4.0)]
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FMap [("x", FInt 1L); ("y", FFloat 2.5)];
        FMap [("x", FInt 3L); ("y", FFloat 4.0)]
    ]
    ignore my_data
