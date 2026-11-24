module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)
capture : a -> b -> c -> d -> e -> f -> g -> ()
capture _ _ _ _ _ _ _ = ()


main : Program () () Never
main =
    let
        _ = capture (EFloat (0 / 0)) (EFloat (1 / 0)) (EFloat (-(1 / 0))) (EFloat 1.25) (EStr "2024-01-15") (EInt 1705322096) (EStr "[ordinary text]")
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
