module Check

type Val =
    | FStr of string
    | FMap of (string * Val) list
let private _checkDeclaration () =
    let mutable my_data: Val = FMap [
        ("key", FStr "\"bang!\"")  // real
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FMap [
        ("key", FStr "\"bang!\"")  // real
    ]
    ignore my_data
