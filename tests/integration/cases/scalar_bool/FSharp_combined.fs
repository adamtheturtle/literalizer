module Check

type Val =
    | FBool of bool
let private _checkDeclaration () =
    let mutable my_data: Val = FBool true
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FBool true
    ignore my_data
