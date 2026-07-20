module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
make_widget :: Json -> Unit
make_widget _ = unit


my_data = make_widget (fromRight jsonNull (jsonParser "42"))
