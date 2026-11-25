module Check exposing (..)


import Json.Encode
make_widget : a -> Json.Encode.Value
make_widget _ = Json.Encode.null


main : Program () () Never
main =
    let
        _ = make_widget (Json.Encode.int 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
