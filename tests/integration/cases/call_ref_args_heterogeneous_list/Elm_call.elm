module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
process : ( a, b ) -> ()
process _ = ()


main : Program () () Never
main =
    let
        my_ints : Val
        my_ints = EList [
            EInt 1,
            EInt 2,
            EInt 3
            ]
        my_strings : Val
        my_strings = EList [
            EStr "a",
            EStr "b"
            ]
        _ = process(my_ints, EInt 42)
        _ = process(my_strings, EInt 7)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
