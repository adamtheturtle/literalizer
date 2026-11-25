{-# LANGUAGE QuasiQuotes #-}
module Fixture_long_string_before_list_comma_Haskell_json_type_aeson_value where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| ["This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.", 1] |]
main :: IO ()
main = seq my_data (return ())
