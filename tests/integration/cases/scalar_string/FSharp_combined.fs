module Check

type Val =
    | FStr of string
let private _checkDeclaration () =
    let mutable my_data: Val = FStr "hello"
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FStr "hello"
    ignore my_data
