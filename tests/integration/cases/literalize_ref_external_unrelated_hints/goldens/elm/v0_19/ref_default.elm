module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
consume_widget : a -> ()
consume_widget _ = ()


main : Program () () Never
main =
    let
        missing : Val
        missing = EList [
            EInt 1,
            EInt 2
            ]
        my_data : Val
        my_data = missing
        _ = consume_widget my_data
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
