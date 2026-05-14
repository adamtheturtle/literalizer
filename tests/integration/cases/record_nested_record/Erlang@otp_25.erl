-module(fixture_record_nested_record_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "id" => 1,
        "owner" => #{"name" => "Alice", "age" => 30}
    },
    My_data.
