{-# LANGUAGE QuasiQuotes #-}
module Fixture_string_control_escape_before_hex_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "a\u0007face" |]
main :: IO ()
main = seq my_data (return ())
