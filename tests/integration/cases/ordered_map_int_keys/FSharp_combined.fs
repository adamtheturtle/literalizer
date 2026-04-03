module Check

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        ("1", FStr "one");
        ("2", FStr "two");
        ("42", FStr "answer")
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        ("1", FStr "one");
        ("2", FStr "two");
        ("42", FStr "answer")
    ]
    ignore my_data
