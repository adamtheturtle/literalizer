module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
make_widget :: Json -> Unit
make_widget _ = unit


main :: Unit
main =
    let
        _ = make_widget (fromRight jsonNull (jsonParser "1"))
    in
    unit
