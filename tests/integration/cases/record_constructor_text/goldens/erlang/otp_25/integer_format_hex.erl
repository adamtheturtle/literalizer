-module(fixture_record_constructor_text_erlang_integer_format_hex).
-export([x/0]).
x() ->
    My_data = #{
        "text" => "Record0(",
        "number" => 16#1
    },
    My_data.
