module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FList [
        FMap [("first", FStr "Alice"); ("last", FStr "Smith")];
        FMap [("first", FStr "Bob"); ("last", FStr "Jones")]
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FList [
        FMap [("first", FStr "Alice"); ("last", FStr "Smith")];
        FMap [("first", FStr "Bob"); ("last", FStr "Jones")]
    ]
    ignore my_data
