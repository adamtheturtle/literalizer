module Check exposing (..)


import Json.Encode
process : a -> Json.Encode.Value
process _ = Json.Encode.null


main : Program () () Never
main =
    let
        unknown_value : Json.Encode.Value
        unknown_value = Json.Encode.list identity []
        _ = process (Json.Encode.list identity [unknown_value])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
