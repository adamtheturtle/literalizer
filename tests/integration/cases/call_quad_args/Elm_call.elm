module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : a -> b -> c -> d -> ()
process _ _ _ _ = ()


main : Program () () Never
main =
    let
        _ = process (EInt 1) (EInt 2) (EInt 3) (EInt 4)
        _ = process (EInt 5) (EInt 6) (EInt 7) (EInt 8)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
