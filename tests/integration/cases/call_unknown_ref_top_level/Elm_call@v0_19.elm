module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        unknown_value : Val
        unknown_value = EList [
            EInt 1
            ]
        _ = process unknown_value
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
