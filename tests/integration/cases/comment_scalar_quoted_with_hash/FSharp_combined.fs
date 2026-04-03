module Check

type Val =
    | FStr of string
// note
let private _checkDeclaration () =
    let mutable my_data: Val = FStr "hello # world"
    ignore my_data

let private _checkAssignment () =
    // note
    let my_data: Val = FStr "hello # world"
    ignore my_data
