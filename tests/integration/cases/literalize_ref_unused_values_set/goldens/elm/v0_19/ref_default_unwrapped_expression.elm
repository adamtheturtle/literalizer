module Check exposing (..)


type Val
    = EInt Int
    | ESet (List Val)
consume_widget : a -> ()
consume_widget _ = ()


main : Program () () Never
main =
    let
        _ = consume_widget (ESet [
            EInt 1,
            EInt 2
            ])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
