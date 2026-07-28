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
        _ = process (EStr "09:30:00")
        _ = process (EStr "2024-01-15T00:00:00+00:00")
        _ = process (EInt 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
