module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"times\": [\"09:30:00\", \"17:45:00\", \"23:59:59\"]}")
