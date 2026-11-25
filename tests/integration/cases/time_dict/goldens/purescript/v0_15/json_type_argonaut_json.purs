module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"morning\": \"09:30:00\", \"afternoon\": \"14:15:00\", \"evening\": \"23:59:59\"}")
