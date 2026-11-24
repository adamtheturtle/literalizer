{-# LANGUAGE QuasiQuotes #-}
module Fixture_control_character_map_keys_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"": 1, "a\u0001b": 2} |]
main :: IO ()
main = seq my_data (return ())
