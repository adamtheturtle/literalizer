module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("flow", FList [
            FInt 1L;
            // After the first element.
            FInt 2L
        ]);
        // Between the key and its value.
        ("gap", FInt 3L);
        // On the block scalar header.
        ("block", FStr "Text.\n");
        ("nested", FList [
            FInt 1L;
            FInt 1L
            // On the nested alias.
        ]);
        ("anchored", FInt 4L);
        ("alias", FInt 4L)
        // On the alias.
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("flow", FList [
            FInt 1L;
            // After the first element.
            FInt 2L
        ]);
        // Between the key and its value.
        ("gap", FInt 3L);
        // On the block scalar header.
        ("block", FStr "Text.\n");
        ("nested", FList [
            FInt 1L;
            FInt 1L
            // On the nested alias.
        ]);
        ("anchored", FInt 4L);
        ("alias", FInt 4L)
        // On the alias.
    ]
    ignore my_data
