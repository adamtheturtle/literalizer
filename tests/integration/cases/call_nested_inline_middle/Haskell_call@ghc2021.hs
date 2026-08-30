module Fixture_call_nested_inline_middle_Haskell_call where
data Val = HStr String | HList [Val]
f :: Val -> IO ()
f _ = return ()
main :: IO ()
main = do
    _ <- f (HList [HList [HStr "DEL", HStr "b", HStr "10"], HList [HStr "ADD", HStr "a", HStr "x"]])  -- note
    pure ()
