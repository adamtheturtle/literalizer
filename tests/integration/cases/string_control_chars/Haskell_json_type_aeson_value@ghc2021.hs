{-# LANGUAGE QuasiQuotes #-}
module Fixture_string_control_chars_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["line1\r\nline2", "line1\rline2", "\u0001"] |]
main :: IO ()
main = seq my_data (return ())
