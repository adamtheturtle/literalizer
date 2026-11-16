module Main

type Val =
    | FInt of int64
    | FList of Val list
let mutable eventIndex = 0
let observeEvent (actual: int64) =
    let expected = [| 1L; 42L; 2L; 142L |]
    if eventIndex >= 4 || actual <> expected[eventIndex] then failwith "receiver event changed"
    eventIndex <- eventIndex + 1
let ``make_widget`` (value) =
    match value with
    | FInt value -> observeEvent 1L; observeEvent value; FInt (value + 100L)
    | _ -> failwith "integer argument required"
let ``consume`` (value) =
    match value with
    | FInt value -> observeEvent 2L; observeEvent value
    | _ -> failwith "integer argument required"
let verify_events () =
    if eventIndex <> 4 then failwith "missing receiver events"
let my_data = make_widget(FInt 42L)
consume(my_data) |> ignore
verify_events() |> ignore
