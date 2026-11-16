module Main

type Val =
    | FInt of int64
    | FList of Val list
let mutable eventIndex = 0
let observeEvent (actual: int64) =
    let expected = [| 1L; 42L; 1L; 42L; 1L; 142L |]
    if eventIndex >= 6 || actual <> expected[eventIndex] then failwith "receiver event changed"
    eventIndex <- eventIndex + 1
let ``make_widget`` (count) =
    match count with
    | FInt value -> observeEvent 1L; observeEvent value; FInt (value + 100L)
    | _ -> failwith "integer argument required"
let verify_events () =
    if eventIndex <> 6 then failwith "missing receiver events"
do
    let mutable my_data: Val = FInt 42L
    make_widget(my_data) |> ignore
    let my_data = make_widget(my_data)
    make_widget(my_data) |> ignore
    verify_events() |> ignore
    ()
