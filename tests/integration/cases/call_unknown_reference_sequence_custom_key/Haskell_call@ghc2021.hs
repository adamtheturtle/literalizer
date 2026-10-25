module Fixture_call_unknown_reference_sequence_custom_key_Haskell_call where
data Val = HList [Val]
process :: Val -> IO ()
process _ = return ()
untypedValue :: Val
untypedValue = HList []
main :: IO ()
main = do
    _ <- process (HList [untypedValue, untypedValue])
    pure ()
