{-# LANGUAGE QuasiQuotes #-}
module Fixture_scalar_int_very_large_Haskell_json_type_aeson_value_bigint where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| 9223372036854775808 |]
main :: IO ()
main = seq my_data (return ())
