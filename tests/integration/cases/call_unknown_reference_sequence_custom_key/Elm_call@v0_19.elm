module Check exposing (..)


type Val
    = EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        untypedValue : Val
        untypedValue = EList []
        _ = process (EList [untypedValue, untypedValue])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
