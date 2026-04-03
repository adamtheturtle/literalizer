module Check

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        // Configuration
        ("name", FStr "app");
        // Port setting
        ("port", FInt 3000L)
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        // Configuration
        ("name", FStr "app");
        // Port setting
        ("port", FInt 3000L)
    ]
    ignore my_data
