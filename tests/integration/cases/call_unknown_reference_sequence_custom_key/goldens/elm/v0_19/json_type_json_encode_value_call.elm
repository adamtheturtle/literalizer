module Check exposing (..)


import Json.Encode
process : a -> Json.Encode.Value
process _ = Json.Encode.null


main : Program () () Never
main =
    let
        untypedValue : Json.Encode.Value
        untypedValue = Json.Encode.list identity []
        _ = process (Json.Encode.list identity [untypedValue, untypedValue])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
