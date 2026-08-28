module Check exposing (..)


record_entry : a -> b -> c -> ()
record_entry _ _ _ = ()
type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)


main : Program () () Never
main =
    let
        my_data = record_entry (EStr "a") (EInt 1) (EBool True)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
