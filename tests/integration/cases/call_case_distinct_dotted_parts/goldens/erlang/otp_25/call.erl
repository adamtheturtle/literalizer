-module(fixture_call_case_distinct_dotted_parts_erlang_call).
-export([x/0]).
'a.foo.Foo.bar'(_) -> ok.
x() ->
    'a.foo.Foo.bar'([1]).
