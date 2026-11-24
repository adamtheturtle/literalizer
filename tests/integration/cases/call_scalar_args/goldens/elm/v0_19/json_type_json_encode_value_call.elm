module Check exposing (..)


import Json.Encode
process : a -> Json.Encode.Value
process _ = Json.Encode.null


main : Program () () Never
main =
    let
        _ = process (Json.Encode.string "hello")
        _ = process (Json.Encode.int 42)
        _ = process (Json.Encode.bool True)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
