module Main

type Val =
    | FInt of int64
    | FList of Val list
let mutable eventIndex = 0
let observeEvent (actual: int64) =
    let expected = [| 1L; 1L |]
    if eventIndex >= 2 || actual <> expected[eventIndex] then failwith "receiver event changed"
    eventIndex <- eventIndex + 1
let ``process`` (value: Val) =
    match value with
    | FInt value -> observeEvent 1L; observeEvent value; FInt (value + 100L)
    | _ -> failwith "integer argument required"
let verify_events () =
    if eventIndex <> 2 then failwith "missing receiver events"
``process``(FInt 1L) |> ignore
verify_events() |> ignore
