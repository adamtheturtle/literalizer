module Check

type Val =
    | FSet of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FSet []
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FSet []
    ignore my_data
