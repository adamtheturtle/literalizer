{-# LANGUAGE QuasiQuotes #-}
module Fixture_multiline_string_nested_list_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [["\nfirst line\n  indented\n\nlast line\n"]] |]
main :: IO ()
main = seq my_data (return ())
