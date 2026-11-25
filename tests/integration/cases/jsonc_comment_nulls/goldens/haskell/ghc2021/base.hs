module Fixture_jsonc_comment_nulls_Haskell where
data Val = HNull | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    -- null heading
    -- before null
    ("a", HNull),  -- first null
    ("b", HNull)  -- second null
    ]
main :: IO ()
main = seq my_data (return ())
