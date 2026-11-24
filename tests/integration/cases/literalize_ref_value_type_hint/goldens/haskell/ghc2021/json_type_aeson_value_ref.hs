{-# LANGUAGE QuasiQuotes #-}
module Fixture_literalize_ref_value_type_hint_Haskell_json_type_aeson_value_ref where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
refData :: Value
refData = [aesonQQ| [1, 2] |]
my_data :: Value
my_data = refData
main :: IO ()
main = seq my_data (return ())
