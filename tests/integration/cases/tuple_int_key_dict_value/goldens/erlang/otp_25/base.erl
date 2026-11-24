-module(fixture_tuple_int_key_dict_value_erlang).
-export([x/0]).
x() ->
    My_data = #{
        1 => [1, "email", "a@gmail.com", 100]
    },
    My_data.
