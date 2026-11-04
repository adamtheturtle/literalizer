module Check exposing (..)


f : a -> ()
f _ = ()
type Val
    = EList (List Val)


main : Program () () Never
main =
    let
        _ = f (EList [])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
