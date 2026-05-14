module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EFloat Float
    | EList (List Val)
process : a -> b -> ()
process _ _ = ()


main : Program () () Never
main =
    let
        my_int : Val
        my_int = EInt 1
        my_bool : Val
        my_bool = EBool True
        my_float : Val
        my_float = EFloat 3.14
        my_list : Val
        my_list = EList [
            EInt 1,
            EInt 2,
            EInt 3
            ]
        _ = process my_int (EInt 42)
        _ = process my_bool (EInt 7)
        _ = process my_float (EInt 9)
        _ = process my_list (EInt 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
