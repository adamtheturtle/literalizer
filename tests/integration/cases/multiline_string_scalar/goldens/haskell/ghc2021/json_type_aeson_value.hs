{-# LANGUAGE QuasiQuotes #-}
module Fixture_multiline_string_scalar_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "\nroot first line\n  indented\n\nroot last line\n" |]
main :: IO ()
main = seq my_data (return ())
