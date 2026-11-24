{-# LANGUAGE QuasiQuotes #-}
module Fixture_nested_empty_map_sibling_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [{"mapping": {}}, {}] |]
main :: IO ()
main = seq my_data (return ())
