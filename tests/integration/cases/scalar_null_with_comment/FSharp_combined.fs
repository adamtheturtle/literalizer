module Check

type Val =
    | FNull
// note
let private _checkDeclaration () =
    let mutable my_data: Val = FNull
    ignore my_data

let private _checkAssignment () =
    // note
    let my_data: Val = FNull
    ignore my_data
