module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let private _mainDeclaration () =
    let mutable my_data: Val = FMap [
        ("user_name", FInt 1L);
        ("user.name", FInt 2L);
        ("user-name", FInt 3L);
        ("field_name_that_is_really_quite_long_one", FInt 4L);
        ("field_name_that_is_really_quite_long_two", FInt 5L)
    ]
    ignore my_data

let private _mainAssignment () =
    let my_data: Val = FMap [
        ("user_name", FInt 1L);
        ("user.name", FInt 2L);
        ("user-name", FInt 3L);
        ("field_name_that_is_really_quite_long_one", FInt 4L);
        ("field_name_that_is_really_quite_long_two", FInt 5L)
    ]
    ignore my_data
