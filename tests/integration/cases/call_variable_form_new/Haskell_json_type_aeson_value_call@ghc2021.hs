{-# LANGUAGE QuasiQuotes #-}
{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_call_variable_form_new_Haskell_json_type_aeson_value_call where
make_widget :: Value -> IO Value
make_widget _ = return undefined
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
my_data = make_widget [aesonQQ| 42 |]
main :: IO ()
main = seq my_data (return ())
