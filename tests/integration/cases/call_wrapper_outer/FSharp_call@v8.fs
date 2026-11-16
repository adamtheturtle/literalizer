module Main

type Val =
    | FInt of int64
    | FList of Val list
let mutable eventIndex = 0
let observeEvent (actual: int64) =
    let expected = [| 1L; 42L; 2L; 142L |]
    if eventIndex >= 4 || actual <> expected[eventIndex] then failwith "receiver event changed"
    eventIndex <- eventIndex + 1
let ``process`` (value: Val) =
    match value with
    | FInt value -> observeEvent 1L; observeEvent value; FInt (value + 100L)
    | _ -> failwith "integer argument required"
let ``emit`` (value: Val) =
    match value with
    | FInt value -> observeEvent 2L; observeEvent value
    | _ -> failwith "integer argument required"
let verify_events () =
    if eventIndex <> 4 then failwith "missing receiver events"
emit(``process``(FInt 42L)) |> ignore
verify_events() |> ignore
