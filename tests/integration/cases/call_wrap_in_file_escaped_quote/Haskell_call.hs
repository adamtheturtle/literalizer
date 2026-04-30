module Fixture_call_wrap_in_file_escaped_quote_Haskell_call where
process :: Val -> IO ()
process _ = return ()
data Val = HStr String | HList [Val]
main :: IO ()
main = do
    _ <- process(HStr "a\"b")
    pure ()
