module Check exposing (..)


ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff : a -> ()
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff _ = ()
type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (EInt 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
