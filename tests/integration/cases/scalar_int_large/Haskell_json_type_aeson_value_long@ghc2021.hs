{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_int_large_Haskell_json_type_aeson_value_long where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| 2147483648 |]
main :: IO ()
main = seq my_data (return ())
