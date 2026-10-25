module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
consume_widget : a -> ()
consume_widget _ = ()


main : Program () () Never
main =
    let
        a : Val
        a = EInt 0
        my_data : Val
        my_data = EList [
            a,
            EInt 1
            ]
        _ = consume_widget my_data
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
