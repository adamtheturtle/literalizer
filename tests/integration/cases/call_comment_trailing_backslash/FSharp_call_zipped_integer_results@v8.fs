module Main

type Val =
    | FInt of int64
    | FList of Val list
let mutable eventIndex = 0
let observeEvent (actual: int64) =
    let expected = [| 1L; 1L; 2L; 101L; 3L; 41L; 1L; 2L; 2L; 102L; 3L; 42L |]
    if eventIndex >= 12 || actual <> expected[eventIndex] then failwith "receiver event changed"
    eventIndex <- eventIndex + 1
let ``process`` (value: Val) =
    match value with
    | FInt value -> observeEvent 1L; observeEvent value; FInt (value + 100L)
    | _ -> failwith "integer argument required"
let ``emit`` (actual: Val, zipped: Val) =
    match actual, zipped with
    | FInt value, FInt companion -> observeEvent 2L; observeEvent value; observeEvent 3L; observeEvent companion
    | _ -> failwith "integer argument required"
let verify_events () =
    if eventIndex <> 12 then failwith "missing receiver events"
emit(``process``(FInt 1L), FInt 41L) |> ignore
emit(``process``(FInt 2L), FInt 42L) |> ignore
verify_events() |> ignore
