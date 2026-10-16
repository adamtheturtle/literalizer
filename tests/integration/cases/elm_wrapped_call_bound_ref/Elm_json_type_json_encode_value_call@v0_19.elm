module Check exposing (..)


import Json.Encode
make_widget : a -> Json.Encode.Value
make_widget _ = Json.Encode.null


main : Program () () Never
main =
    let
        value : Json.Encode.Value
        value = Json.Encode.int 1
        _ = make_widget value
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
