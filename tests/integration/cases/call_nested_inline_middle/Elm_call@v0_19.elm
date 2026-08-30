module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
f : a -> ()
f _ = ()


main : Program () () Never
main =
    let
        _ = f (EList [EList [EStr "DEL", EStr "b", EStr "10"], EList [EStr "ADD", EStr "a", EStr "x"]])  -- note
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
