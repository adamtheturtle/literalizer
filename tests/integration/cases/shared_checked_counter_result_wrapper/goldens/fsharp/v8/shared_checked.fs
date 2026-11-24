module Fixture_shared_checked_counter_result_wrapper_FSharp_shared_checked

type Val =
    | FBool of bool
    | FFloat of float
    | FStr of string
    | FList of Val list
type Counter() =
    let mutable calls = 0
    member _.Calls = calls
    member _.accept(user: Val, timestamp: Val) =
        match user, timestamp with
        | FStr text, FFloat value ->
            if text <> (if calls = 0 then "user_1" else "user_2") || value <> 100.0 + float calls then failwith "receiver arguments changed"
            calls <- calls + 1
            text = "user_1"
        | _ -> failwith "receiver argument types changed"
let mutable checks = 0
let checkResult(actual: bool, expected: Val) =
    match expected with
    | FList [FBool wanted; FStr reason] ->
        if actual <> wanted || reason <> (if checks = 0 then "first" else "second") then failwith "paired result changed"
        checks <- checks + 1
    | _ -> failwith "paired result types changed"
let counter = Counter()
checkResult(counter.accept(FStr "user_1", FFloat 100.0), FList [FBool true; FStr "first"]) |> ignore
if counter.Calls <> 1 || checks <> 1 then failwith "calls skipped"
