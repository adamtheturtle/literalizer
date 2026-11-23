{-# LANGUAGE QuasiQuotes #-}
module Fixture_call_json_nested_ref_array_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
consume :: Value -> IO ()
consume _ = return ()
shared :: Value
shared = [aesonQQ| [1, 2] |]
main :: IO ()
main = do
    _ <- consume [aesonQQ| [#{shared}, 42] |]
    pure ()
