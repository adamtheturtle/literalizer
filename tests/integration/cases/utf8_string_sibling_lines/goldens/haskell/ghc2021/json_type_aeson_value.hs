{-# LANGUAGE QuasiQuotes #-}
module Fixture_utf8_string_sibling_lines_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["中中中中中中中中中中中中中中中中中中中中", "é'é'é'é'é'é'é'é'é'é'", "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"] |]
main :: IO ()
main = seq my_data (return ())
