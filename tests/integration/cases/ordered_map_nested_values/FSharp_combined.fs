module Check

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        ("name", FStr "Alice");
        ("scores", FMap [("1", FStr "first"); ("2", FStr "second")])
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        ("name", FStr "Alice");
        ("scores", FMap [("1", FStr "first"); ("2", FStr "second")])
    ]
    ignore my_data
