-module(fixture_record_empty_dict_field_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "f" => #{},
        "g" => 1
    },
    My_data.
