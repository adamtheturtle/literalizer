-module(fixture_dict_with_hyphen_keys_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "my-key" => "value1",
        "another-key" => "value2",
        "normal_key" => "value3"
    },
    My_data.
