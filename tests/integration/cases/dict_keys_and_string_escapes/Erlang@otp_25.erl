-module(fixture_dict_keys_and_string_escapes_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "plain" => [1, 2],
        "with-dash" => "a\nb"
    },
    My_data.
