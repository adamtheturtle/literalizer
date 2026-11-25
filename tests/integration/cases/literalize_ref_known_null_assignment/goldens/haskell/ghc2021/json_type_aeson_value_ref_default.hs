{-# LANGUAGE QuasiQuotes #-}
module Fixture_literalize_ref_known_null_assignment_Haskell_json_type_aeson_value_ref_default where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
item :: Value
item = [aesonQQ| null |]
my_data :: Value
my_data = item
main :: IO ()
main = seq my_data (return ())
