module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
f : a -> b -> ()
f _ _ = ()


main : Program () () Never
main =
    let
        _ = f (EInt 2) (EStr "hello")  -- trailing note
        _ = f (EInt 3) (EStr "world")  -- another note
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
