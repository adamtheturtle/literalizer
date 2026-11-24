module Fixture_call_whole_empty_list_argument_Haskell_call where
f :: Val -> IO ()
f _ = return ()
data Val = HList [Val]
main :: IO ()
main = do
    _ <- f (HList [])
    pure ()
