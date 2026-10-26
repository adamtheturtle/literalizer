{-# LANGUAGE QuasiQuotes #-}
module Fixture_widened_i64_minimum_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [-9223372036854775808, 5] |]
main :: IO ()
main = seq my_data (return ())
