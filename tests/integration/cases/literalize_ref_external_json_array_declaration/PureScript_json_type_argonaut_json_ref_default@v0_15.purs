module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
consume_widget :: Json -> Unit
consume_widget _ = unit
shared :: Json
shared = fromRight jsonNull (jsonParser "[1, 2]")
my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"$ref\": \"shared\"}")


main :: Unit
main =
    let
        _ = consume_widget my_data
    in
    unit
