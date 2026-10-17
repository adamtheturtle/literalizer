{-# LANGUAGE QuasiQuotes #-}
module Fixture_elm_wrapped_call_bound_ref_Haskell_json_type_aeson_value_call where
import Data.Aeson (Value)
import Data.Aeson.QQ (aesonQQ)
make_widget :: Value -> IO ()
make_widget _ = return ()
value :: Value
value = [aesonQQ| 1 |]
main :: IO ()
main = do
    _ <- make_widget value
    pure ()
