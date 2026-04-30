module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : ( a, b ) -> ()
process _ = ()


main : Program () () Never
main =
    let
        shared : Val
        shared = EInt 1
        other : Val
        other = EInt 2
        _ = process(shared, EInt 1)
        _ = process(other, EInt 0)
        _ = process(shared, EInt 8)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
