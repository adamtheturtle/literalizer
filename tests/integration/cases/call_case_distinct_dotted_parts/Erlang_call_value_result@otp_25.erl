-module(fixture_call_case_distinct_dotted_parts_erlang_call_value_result).
-export([x/0]).
'a.foo.Foo.bar'(_) -> undefined.
x() ->
    My_data = 'a.foo.Foo.bar'([1]),
    My_data.
