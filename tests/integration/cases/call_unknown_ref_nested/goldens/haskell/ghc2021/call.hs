module Fixture_call_unknown_ref_nested_Haskell_call where
data Val = HBool Bool | HList [Val]
process :: Val -> Val -> IO ()
process _ _ = return ()
known_value :: Val
known_value = HBool True
unknown_value :: Val
unknown_value = HBool True
main :: IO ()
main = do
    _ <- process known_value unknown_value
    pure ()
