{-# LANGUAGE QuasiQuotes #-}
module Fixture_call_unknown_ref_values_nested_list_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
process :: Value -> IO ()
process _ = return ()
unknown_value :: Value
unknown_value = [aesonQQ| [] |]
main :: IO ()
main = do
    _ <- process [aesonQQ| [#{unknown_value}] |]
    pure ()
