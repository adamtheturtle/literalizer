module Check exposing (..)


import Json.Encode
objStd : a -> Json.Encode.Value
objStd _ = Json.Encode.null


main : Program () () Never
main =
    let
        _ = objStd (Json.Encode.int 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
