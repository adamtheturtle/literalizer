module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        _ = -- Test cases
        _ = process(EStr "hello")  -- single word
        _ = process(EStr "hello world")  -- two words
        _ = -- trailing comment
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
