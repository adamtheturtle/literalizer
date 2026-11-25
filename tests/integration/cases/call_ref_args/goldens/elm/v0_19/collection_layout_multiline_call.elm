module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : a -> b -> ()
process _ _ = ()


main : Program () () Never
main =
    let
        my_var : Val
        my_var = EList [
            EInt 1,
            EInt 2,
            EInt 3
            ]
        my_other : Val
        my_other = EList [
            EInt 4,
            EInt 5,
            EInt 6
            ]
        _ = process my_var (EInt 42)
        _ = process my_other (EInt 7)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
