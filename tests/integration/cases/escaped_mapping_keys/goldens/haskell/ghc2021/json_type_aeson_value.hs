{-# LANGUAGE QuasiQuotes #-}
module Fixture_escaped_mapping_keys_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"quote\"backslash\\": 1, "line\nbreak": 2, "$(literal)${text}": 3, "RStr prefix": 4} |]
main :: IO ()
main = seq my_data (return ())
