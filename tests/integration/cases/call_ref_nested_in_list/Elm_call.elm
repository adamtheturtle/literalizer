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
        my_var : Val
        my_var = EInt 42
        my_other : Val
        my_other = EInt 7
        _ = process(EList [my_var, EInt 42, EStr "static"])
        _ = process(EList [my_other, EInt 7, EStr "label"])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
