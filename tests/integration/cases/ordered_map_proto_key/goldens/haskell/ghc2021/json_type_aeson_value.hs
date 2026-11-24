{-# LANGUAGE QuasiQuotes #-}
module Fixture_ordered_map_proto_key_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"__proto__": {"x": 1}, "ordinary": 2} |]
main :: IO ()
main = seq my_data (return ())
