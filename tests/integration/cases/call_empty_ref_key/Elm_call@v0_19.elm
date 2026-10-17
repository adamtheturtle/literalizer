module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
consume : a -> ()
consume _ = ()


main : Program () () Never
main =
    let
        external_value : Val
        external_value = EInt 1
        _ = consume external_value
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
