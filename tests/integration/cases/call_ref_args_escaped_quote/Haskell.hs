module Fixture_call_ref_args_escaped_quote_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HList [HMap [("$ref", HStr "my_str")]]
    ]
main :: IO ()
main = seq my_data (return ())
