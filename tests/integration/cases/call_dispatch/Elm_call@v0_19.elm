module Check exposing (..)


put : a -> b -> ()
put _ _ = ()
get : a -> ()
get _ = ()
type Val
    = EInt Int
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = put (EInt 1) (EInt 10)
        _ = get (EInt 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
