module Check exposing (..)


process : a -> ()
process _ = ()
type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = process (EList [
            EInt 1,
            EInt 2
            ])
        _ = process (EList [
            EInt 3
            ])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
