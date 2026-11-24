-module(fixture_record_nested_container_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "title" => "report",
        "tags" => ["draft", "urgent", "review"],
        "priority" => 2
    },
    My_data.
