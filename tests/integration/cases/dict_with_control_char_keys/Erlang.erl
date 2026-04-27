-module(fixture_dict_with_control_char_keys_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "key\nwith\nnewlines" => "value1",
        "key\twith\ttabs" => "value2",
        "" => "value3"
    },
    My_data.
