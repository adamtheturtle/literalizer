module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("times", FList [FStr (string (System.TimeOnly(9, 30, 0))); FStr (string (System.TimeOnly(17, 45, 0))); FStr (string (System.TimeOnly(23, 59, 59)))])
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("times", FList [FStr (string (System.TimeOnly(9, 30, 0))); FStr (string (System.TimeOnly(17, 45, 0))); FStr (string (System.TimeOnly(23, 59, 59)))])
    ]
    ignore my_data
