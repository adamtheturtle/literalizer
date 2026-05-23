{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_float_Haskell_json_type_aeson_value_float where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| 3.14 |]
main :: IO ()
main = seq my_data (return ())
