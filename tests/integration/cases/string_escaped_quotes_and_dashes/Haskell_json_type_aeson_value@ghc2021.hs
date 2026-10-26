{-# LANGUAGE QuasiQuotes #-}
module Fixture_string_escaped_quotes_and_dashes_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| "hello \"world\" -- not a comment" |]
main :: IO ()
main = seq my_data (return ())
