module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        _ = process (EStr "Dune")  -- first edition
        _ = process (EStr "Solaris")
        _ = process (EStr "Neuromancer")  -- cyberpunk
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
