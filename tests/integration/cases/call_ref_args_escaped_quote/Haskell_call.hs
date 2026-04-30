module Fixture_call_ref_args_escaped_quote_Haskell_call where
data Val = HStr String | HList [Val]
process :: Val -> IO ()
process _ = return ()
my_str :: Val
my_str = HStr "a\"b"
main :: IO ()
main = do
    _ <- process(my_str)
    pure ()
