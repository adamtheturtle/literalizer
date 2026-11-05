{-# LANGUAGE QuasiQuotes #-}
module Fixture_string_nul_before_hex_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"x": "before\u0000after"} |]
main :: IO ()
main = seq my_data (return ())
