module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : a -> b -> ()
process _ _ = ()


main : Program () () Never
main =
    let
        _ = process (EInt 1) (EInt 42)
        _ = process (EInt 2) (EInt 100)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
