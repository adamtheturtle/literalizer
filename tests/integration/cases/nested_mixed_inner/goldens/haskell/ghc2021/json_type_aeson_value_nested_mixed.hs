{-# LANGUAGE QuasiQuotes #-}
module Fixture_nested_mixed_inner_Haskell_json_type_aeson_value_nested_mixed where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [[1, "a"], [2, "b"]] |]
main :: IO ()
main = seq my_data (return ())
