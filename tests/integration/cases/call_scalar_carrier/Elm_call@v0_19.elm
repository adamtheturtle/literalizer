module Check exposing (..)


process : a -> ()
process _ = ()
type Val
    = ENull
    | EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = process (EStr "hello")
        _ = process (EInt 42)
        _ = process (EBool True)
        _ = process (ENull)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
