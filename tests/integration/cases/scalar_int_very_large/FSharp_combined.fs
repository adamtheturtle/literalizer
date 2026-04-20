module Check

type Val =
    | FInt of bigint
let private _checkDeclaration () =
    let mutable my_data: Val = FInt 9223372036854775808I
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FInt 9223372036854775808I
    ignore my_data
