module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"test\": [5, [\"compile\", \"test\"]], \"package\": [7, [\"link\", \"test\"]]}")
