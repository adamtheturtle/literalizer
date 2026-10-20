module Fixture_call_ref_null_consumable_Haskell_call where
data Val = HNull | HList [Val]
consume :: Val -> IO ()
consume _ = return ()
my_null :: Val
my_null = HNull
regular_null :: Val
regular_null = HNull
main :: IO ()
main = do
    _ <- consume my_null
    _ <- consume regular_null
    pure ()
