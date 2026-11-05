module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"exact_millisecond\": \"09:30:15.123000\", \"sub_millisecond\": \"09:30:15.123456\"}")
