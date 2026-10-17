{-# LANGUAGE QuasiQuotes #-}
module Fixture_elm_wrapped_call_scalar_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
make_widget :: Value -> IO ()
make_widget _ = return ()
main :: IO ()
main = do
    _ <- make_widget [aesonQQ| 1 |]
    pure ()
