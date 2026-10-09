module Check exposing (..)


process : a -> b -> ()
process _ _ = ()
type Val
    = ENull
    | EBool Bool
    | EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)


main : Program () () Never
main =
    let
        _ = process (EInt 1) (EStr "hello")
        _ = process (EStr "two") (EBool False)
        _ = process (EFloat 3.5) (ENull)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
