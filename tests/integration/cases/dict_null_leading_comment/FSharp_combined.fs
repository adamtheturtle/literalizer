module Check

type Val =
    | FNull
    | FStr of string
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        // comment
        ("name", FStr "Alice");
        ("score", FNull)
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        // comment
        ("name", FStr "Alice");
        ("score", FNull)
    ]
    ignore my_data
