module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
consume :: Json -> Unit
consume _ = unit
shared :: Json
shared = fromRight jsonNull (jsonParser "null")


main :: Unit
main =
    let
        _ = consume (fromRight jsonNull (jsonParser "{\"left\": {\"$ref\": \"shared\"}, \"nested\": [{\"$ref\": \"shared\"}]}"))
    in
    unit
