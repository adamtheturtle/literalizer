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
        my_empty : Val
        my_empty = EList []
        _ = process(my_ints, EInt 42)
        _ = process(my_strings, EInt 7)
        _ = process(my_empty, EInt 99)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
