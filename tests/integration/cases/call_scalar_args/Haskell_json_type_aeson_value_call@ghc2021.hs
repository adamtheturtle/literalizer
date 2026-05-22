{-# LANGUAGE OverloadedStrings #-}
module Fixture_call_scalar_args_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value, eitherDecodeStrict)
import Data.Text.Encoding (encodeUtf8)
process :: Value -> IO ()
process _ = return ()
main :: IO ()
main = do
    _ <- process (either error id (eitherDecodeStrict (encodeUtf8 "\"hello\"")))
    _ <- process (either error id (eitherDecodeStrict (encodeUtf8 "42")))
    _ <- process (either error id (eitherDecodeStrict (encodeUtf8 "true")))
    pure ()
