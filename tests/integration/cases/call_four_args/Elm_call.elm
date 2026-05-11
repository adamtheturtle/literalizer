module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : a -> b -> c -> d -> ()
process _ _ _ _ = ()


main : Program () () Never
main =
    let
        _ = process(EInt 1, EInt 2, EInt 3, EInt 4)
        _ = process(EInt 10, EInt 20, EInt 30, EInt 40)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
