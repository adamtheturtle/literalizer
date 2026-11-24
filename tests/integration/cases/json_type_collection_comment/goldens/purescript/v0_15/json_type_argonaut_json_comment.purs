module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


-- About a.
my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"a\": 1, \"b\": 2}")
