-module(fixture_keyword_prefix_dotted_member_erlang_call).
-export([x/0]).
'thing.first_value'(_) -> ok.
x() ->
    'thing.first_value'(1).
