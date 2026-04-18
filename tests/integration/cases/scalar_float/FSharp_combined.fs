module Check

type Val =
    | FFloat of float
let private _checkDeclaration () =
    let mutable my_data: Val = FFloat 3.14
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FFloat 3.14
    ignore my_data
