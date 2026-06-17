module Check exposing (..)


store_item : a -> b -> ()
store_item _ _ = ()
read_item : a -> ()
read_item _ = ()
type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = store_item (EInt 1) (EInt 10)
        _ = read_item (EInt 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
