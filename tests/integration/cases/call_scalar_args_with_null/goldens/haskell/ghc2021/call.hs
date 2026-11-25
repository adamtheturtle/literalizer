module Fixture_call_scalar_args_with_null_Haskell_call where
data Val = HNull | HStr String | HList [Val]
process :: Val -> IO ()
process _ = return ()
main :: IO ()
main = do
    _ <- process (HNull)
    _ <- process (HStr "hello")
    pure ()
