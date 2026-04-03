module Check

type Val =
    | FStr of string
    | FDate of System.DateTime
let private _checkDeclaration () =
    let mutable my_data: Val = FStr (string (System.DateOnly(2024, 1, 15)))
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FStr (string (System.DateOnly(2024, 1, 15)))
    ignore my_data
