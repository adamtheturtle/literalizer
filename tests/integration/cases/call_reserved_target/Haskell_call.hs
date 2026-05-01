module Fixture_call_reserved_target_Haskell_call where
data Val = HStr String | HList [Val]
op :: Val -> IO ()
op _ = return ()
main :: IO ()
main = do
    _ <- op(HStr "hello")
    pure ()
