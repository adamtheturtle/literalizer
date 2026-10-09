module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
consume :: Json -> Unit
consume _ = unit
item :: Json
item = fromRight jsonNull (jsonParser "\"s\"")


main :: Unit
main =
    let
        _ = consume item
    in
    unit
