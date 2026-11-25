module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
fooClass : a -> ()
fooClass _ = ()


main : Program () () Never
main =
    let
        _ = fooClass (EInt 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
