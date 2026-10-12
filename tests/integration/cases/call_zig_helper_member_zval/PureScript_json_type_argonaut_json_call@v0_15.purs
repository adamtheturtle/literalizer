module Check where


import Prelude
import Data.Argonaut.Core (Json, jsonNull)
import Data.Argonaut.Parser (jsonParser)
import Data.Either (fromRight)
obj :: { ZVal :: Json -> Unit }
obj = { ZVal: \_ -> unit }


main :: Unit
main =
    let
        _ = obj.ZVal (fromRight jsonNull (jsonParser "1"))
    in
    unit
