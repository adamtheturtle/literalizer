module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : ( a, b ) -> ()
process _ = ()


main : Program () () Never
main =
    let
        single_var : Val
        single_var = EList [
            EInt 4,
            EInt 5,
            EInt 6
            ]
        repeated_var : Val
        repeated_var = EInt 1
        _ = process(repeated_var, EInt 1)
        _ = process(single_var, EInt 0)
        _ = process(repeated_var, EInt 8)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
