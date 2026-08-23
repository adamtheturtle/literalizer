module Fixture_call_self_target_Haskell_call where
data Val = HStr String | HList [Val]
self :: Val -> IO ()
self _ = return ()
main :: IO ()
main = do
    _ <- self (HStr "hello")
    pure ()
