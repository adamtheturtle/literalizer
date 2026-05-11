module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
process : ( a, b ) -> ()
process _ = ()


main : Program () () Never
main =
    let
        _ = process(EStr "hello", EStr "a")
        _ = process(EInt 42, EStr "b")
        _ = process(EBool True, EStr "c")
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
