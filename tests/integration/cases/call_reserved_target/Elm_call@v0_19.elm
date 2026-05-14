module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
op : a -> ()
op _ = ()


main : Program () () Never
main =
    let
        _ = op (EStr "hello")
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
