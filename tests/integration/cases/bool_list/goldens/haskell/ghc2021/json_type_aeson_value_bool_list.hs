{-# LANGUAGE QuasiQuotes #-}
module Fixture_bool_list_Haskell_json_type_aeson_value_bool_list where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data :: Value
my_data = [aesonQQ| [true, false, true] |]
main :: IO ()
main = seq my_data (return ())
