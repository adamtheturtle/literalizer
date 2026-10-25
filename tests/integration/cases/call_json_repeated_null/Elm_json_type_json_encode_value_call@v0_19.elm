module Check exposing (..)


import Json.Encode
consume : a -> Json.Encode.Value
consume _ = Json.Encode.null


main : Program () () Never
main =
    let
        shared : Json.Encode.Value
        shared = Json.Encode.null
        _ = consume (Json.Encode.object [("left", shared), ("nested", Json.Encode.list identity [shared])])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
