module Check where


import Prelude
data Val
    = PNull
item :: Val
item = PNull
my_data :: Val
my_data = PNull


main :: Unit
main =
    let
        _ = (void)my_data;
        _ = my_data = item
        _ = (void)my_data;
    in
    unit
