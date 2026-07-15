{-# LANGUAGE QuasiQuotes #-}
module Fixture_binary_Haskell_json_type_aeson_value_bytes_base64 where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["48656c6c6f"] |]
main :: IO ()
main = seq my_data (return ())
