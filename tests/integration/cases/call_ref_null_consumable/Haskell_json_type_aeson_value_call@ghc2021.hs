{-# LANGUAGE QuasiQuotes #-}
module Fixture_call_ref_null_consumable_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
consume :: Value -> IO ()
consume _ = return ()
my_null :: Value
my_null = [aesonQQ| null |]
regular_null :: Value
regular_null = [aesonQQ| null |]
main :: IO ()
main = do
    _ <- consume my_null
    _ <- consume regular_null
    pure ()
