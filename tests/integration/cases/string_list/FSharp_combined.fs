module Check

type Val =
    | FStr of string
    | FList of Val list
let private _checkDeclaration () =
    let mutable my_data: Val = FList [
        FStr "foo";
        FStr "bar";
        FStr "baz"
    ]
    ignore my_data

let private _checkAssignment () =
    let my_data: Val = FList [
        FStr "foo";
        FStr "bar";
        FStr "baz"
    ]
    ignore my_data
