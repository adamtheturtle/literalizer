module Check exposing (..)


import Json.Encode
consume_widget : a -> Json.Encode.Value
consume_widget _ = Json.Encode.null


main : Program () () Never
main =
    let
        shared : Json.Encode.Value
        shared = Json.Encode.list identity [
            Json.Encode.int 1,
            Json.Encode.int 2
            ]
        my_data : Json.Encode.Value
        my_data = shared
        _ = consume_widget my_data
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
