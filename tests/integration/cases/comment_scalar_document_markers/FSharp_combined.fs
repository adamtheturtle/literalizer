module Check

type Val =
    | FInt of int64
// note
let private _checkDeclaration () =
    let mutable my_data: Val = FInt 42L
    ignore my_data

let private _checkAssignment () =
    // note
    let my_data: Val = FInt 42L
    ignore my_data
