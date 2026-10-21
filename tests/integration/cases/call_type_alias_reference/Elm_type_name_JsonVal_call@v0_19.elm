module Check exposing (..)


type JsonVal
    = EInt Int
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        value : JsonVal
        value = EInt 1
        _ = process value
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
