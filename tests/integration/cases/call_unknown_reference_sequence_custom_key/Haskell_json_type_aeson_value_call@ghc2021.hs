{-# LANGUAGE QuasiQuotes #-}
module Fixture_call_unknown_reference_sequence_custom_key_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
process :: Value -> IO ()
process _ = return ()
untypedValue :: Value
untypedValue = [aesonQQ| [] |]
main :: IO ()
main = do
    _ <- process [aesonQQ| [#{untypedValue}, #{untypedValue}] |]
    pure ()
