{-# LANGUAGE QuasiQuotes #-}
module Fixture_dict_proto_key_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"__proto__": {"x": 1}, "n": {"__proto__": 3}, "y": 2} |]
main :: IO ()
main = seq my_data (return ())
