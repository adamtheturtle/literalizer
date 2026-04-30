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
        my_var : Val
        my_var = EInt 42
        _ = process(EDict [("key", my_var), ("count", EInt 42)])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
