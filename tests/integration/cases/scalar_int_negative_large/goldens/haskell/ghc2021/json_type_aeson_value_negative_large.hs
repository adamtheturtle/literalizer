{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_int_negative_large_Haskell_json_type_aeson_value_negative_large where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| -2147483649 |]
main :: IO ()
main = seq my_data (return ())
