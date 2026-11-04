module Check exposing (..)


f : a -> ()
f _ = ()
type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = f (EList [EInt 1, EInt 2])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
