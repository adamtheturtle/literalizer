-module(fixture_call_case_distinct_dotted_parts_erlang_call_root_collision).
-export([x/0]).
'foo.Foo.bar'(_) -> ok.
x() ->
    'foo.Foo.bar'([1]).
