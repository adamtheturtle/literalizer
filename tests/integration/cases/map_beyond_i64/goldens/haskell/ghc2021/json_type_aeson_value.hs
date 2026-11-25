{-# LANGUAGE QuasiQuotes #-}
module Fixture_map_beyond_i64_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| {"a": 9223372036854775807, "b": 9223372036854775808} |]
main :: IO ()
main = seq my_data (return ())
