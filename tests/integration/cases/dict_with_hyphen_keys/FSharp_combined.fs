module Check

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        ("my-key", FStr "value1");
        ("another-key", FStr "value2");
        ("normal_key", FStr "value3")
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        ("my-key", FStr "value1");
        ("another-key", FStr "value2");
        ("normal_key", FStr "value3")
    ]
    ignore my_data
