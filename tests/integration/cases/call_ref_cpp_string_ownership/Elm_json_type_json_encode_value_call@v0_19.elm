module Check exposing (..)


import Json.Encode
consume : a -> Json.Encode.Value
consume _ = Json.Encode.null


main : Program () () Never
main =
    let
        item : Json.Encode.Value
        item = Json.Encode.string "s"
        _ = consume item
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
