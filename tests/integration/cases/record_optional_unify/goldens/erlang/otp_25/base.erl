-module(fixture_record_optional_unify_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "items" => [#{"id" => 1}, #{"id" => 2, "count" => 10}, #{"id" => 3, "count" => 20}]
    },
    My_data.
