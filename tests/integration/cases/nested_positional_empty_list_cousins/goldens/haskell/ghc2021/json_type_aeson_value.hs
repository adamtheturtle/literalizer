{-# LANGUAGE QuasiQuotes #-}
module Fixture_nested_positional_empty_list_cousins_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [[[], []], [[1], [1]]] |]
main :: IO ()
main = seq my_data (return ())
