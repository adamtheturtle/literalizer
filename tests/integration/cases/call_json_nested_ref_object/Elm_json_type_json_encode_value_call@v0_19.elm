module Check exposing (..)


import Json.Encode
consume : a -> Json.Encode.Value
consume _ = Json.Encode.null


main : Program () () Never
main =
    let
        shared : Json.Encode.Value
        shared = Json.Encode.list identity [
            Json.Encode.int 1,
            Json.Encode.int 2
            ]
        _ = consume (Json.Encode.object [("field", shared), ("nested", Json.Encode.list identity [shared, Json.Encode.object []])])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
