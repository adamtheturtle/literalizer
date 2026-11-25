module Check where


import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)


my_data :: Json
my_data = fromRight jsonNull (jsonParser "{\"quote\\\"backslash\\\\\": 1, \"line\\nbreak\": 2, \"$(literal)${text}\": 3, \"RStr prefix\": 4}")
