module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
self : a -> ()
self _ = ()


main : Program () () Never
main =
    let
        _ = self (EStr "hello")
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
