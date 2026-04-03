module Check

type Val =
    | FStr of string
    | FDatetime of System.DateTime
let private _checkDeclaration () =
    let mutable my_data: Val = FStr (string (System.DateTime(2024, 1, 15, 0, 0, 0)))
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FStr (string (System.DateTime(2024, 1, 15, 0, 0, 0)))
    ignore my_data
