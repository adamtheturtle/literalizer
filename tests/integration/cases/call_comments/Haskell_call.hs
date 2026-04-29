module Fixture_call_comments_Haskell_call where
data Val = HStr String | HList [Val]
process :: Val -> IO ()
process _ = return ()
main :: IO ()
main = do
    _ <- -- Test cases
    _ <- process(HStr "hello")  -- single word
    _ <- process(HStr "hello world")  -- two words
    _ <- -- trailing comment
    pure ()
