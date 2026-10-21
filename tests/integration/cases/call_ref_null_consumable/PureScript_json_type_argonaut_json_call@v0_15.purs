module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
consume :: Json -> Unit
consume _ = unit
my_null :: Json
my_null = fromRight jsonNull (jsonParser "null")
regular_null :: Json
regular_null = fromRight jsonNull (jsonParser "null")


main :: Unit
main =
    let
        _ = consume my_null
        _ = consume regular_null
    in
    unit
