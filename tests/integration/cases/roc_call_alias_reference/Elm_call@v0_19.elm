module Check exposing (..)


type Val
    = EInt Int
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        value : Val
        value = EInt 1
        _ = process value
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
