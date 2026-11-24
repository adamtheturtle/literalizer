module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        _ = process (EDict [("value", EInt 1)])
        _ = process (EDict [("value", EStr "hello")])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
