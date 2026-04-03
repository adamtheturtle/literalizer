module Check

type Val =
    | FStr of string
    | FSet of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FSet [
        FStr "apple";  // inline comment
        // before banana
        FStr "banana"
        // trailing
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FSet [
        FStr "apple";  // inline comment
        // before banana
        FStr "banana"
        // trailing
    ]
    ignore my_data
