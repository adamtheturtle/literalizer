module Check exposing (..)


import Json.Encode
consume : a -> Json.Encode.Value
consume _ = Json.Encode.null


main : Program () () Never
main =
    let
        my_null : Json.Encode.Value
        my_null = Json.Encode.null
        regular_null : Json.Encode.Value
        regular_null = Json.Encode.null
        _ = consume my_null
        _ = consume regular_null
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
