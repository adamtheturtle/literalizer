-module(fixture_dict_with_quoted_digit_keys_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "0a" => "first",
        "1b" => "second"
    },
    My_data.
