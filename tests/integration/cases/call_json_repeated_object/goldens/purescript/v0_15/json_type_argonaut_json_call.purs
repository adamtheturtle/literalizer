module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
consume :: Json -> Unit
consume _ = unit
shared :: Json
shared = fromRight jsonNull (jsonParser "{\"value\": [1, 2]}")


main :: Unit
main =
    let
        _ = consume (fromRight jsonNull (jsonParser "{\"left\": {\"$ref\": \"shared\"}, \"right\": {\"$ref\": \"shared\"}}"))
    in
    unit
