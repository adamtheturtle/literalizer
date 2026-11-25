module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("a", FMap [
            ("b", FList [FInt 1L]);
            // Outdented from the sequence, so the inner mapping claims this.
            ("c", FInt 2L)
        ]);
        // Outdented from the inner mapping too, so the root claims this.
        ("d", FInt 3L)
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("a", FMap [
            ("b", FList [FInt 1L]);
            // Outdented from the sequence, so the inner mapping claims this.
            ("c", FInt 2L)
        ]);
        // Outdented from the inner mapping too, so the root claims this.
        ("d", FInt 3L)
    ]
    ignore my_data
