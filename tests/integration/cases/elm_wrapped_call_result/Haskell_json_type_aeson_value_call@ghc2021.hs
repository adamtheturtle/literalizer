{-# LANGUAGE QuasiQuotes #-}
{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_elm_wrapped_call_result_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
make_widget :: Value -> IO Value
make_widget _ = return undefined
my_data = make_widget [aesonQQ| 1 |]
main :: IO ()
main = seq my_data (return ())
