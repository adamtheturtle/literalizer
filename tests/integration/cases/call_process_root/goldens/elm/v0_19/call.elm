module Check exposing (..)


processApiFetch : a -> ()
processApiFetch _ = ()
type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


main : Program () () Never
main =
    let
        _ = processApiFetch (EDict [("data", EStr "hello")])
        _ = processApiFetch (EDict [("data", EInt 42)])
        _ = processApiFetch (EDict [("data", EBool True)])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
