module Main

type Val =
    | FInt of int64
    | FList of Val list
let mutable eventIndex = 0
let observeEvent (actual: int64) =
    let expected = [| 2L; 0L; 1L; 1L; 2L; 101L |]
    if eventIndex >= 6 || actual <> expected[eventIndex] then failwith "receiver event changed"
    eventIndex <- eventIndex + 1
let ``make_widget`` (count) =
    match count with
    | FInt value -> observeEvent 1L; observeEvent value; FInt (value + 100L)
    | _ -> failwith "integer argument required"
let ``consume_widget`` (count) =
    match count with
    | FInt value -> observeEvent 2L; observeEvent value
    | _ -> failwith "integer argument required"
let verify_events () =
    if eventIndex <> 6 then failwith "missing receiver events"
do
    let mutable my_data: Val = FInt 0L
    consume_widget(my_data) |> ignore
    let my_data = make_widget(FInt 1L)
    consume_widget(my_data) |> ignore
    verify_events() |> ignore
    ()
