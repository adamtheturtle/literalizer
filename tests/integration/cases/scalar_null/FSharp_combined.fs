module Check

type Val =
    | FNull
let private _checkDeclaration () =
    let mutable my_data: Val = FNull
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FNull
    ignore my_data
