module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        _ = process (EList [EInt 1, EStr "x"])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
