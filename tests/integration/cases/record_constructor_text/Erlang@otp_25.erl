-module(fixture_record_constructor_text_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "text" => "Record0(",
        "number" => 1
    },
    My_data.
