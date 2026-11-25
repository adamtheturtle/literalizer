module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


refData :: Json
refData = fromRight jsonNull (jsonParser "[1, 2]")
my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"$ref\": \"ref_data\"}")
