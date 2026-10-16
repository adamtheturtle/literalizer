module Fixture_coercion_uniform_dict_shapes_json5_Haskell where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("type", HStr "create"), ("name", HStr "a")],
    HMap [("type", HStr "update"), ("name", HStr "b")]
    ]
main :: IO ()
main = seq my_data (return ())
