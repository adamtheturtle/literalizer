-module(fixture_record_quoted_field_erlang).
-export([x/0]).
x() ->
    My_data = [
        #{"a-b" => 1}
    ],
    My_data.
