module Check exposing (..)


type Val
    = ENull
    | EInt Int
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        _ = process (ENull)
        _ = process (EList [EInt 1, EInt 2])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
