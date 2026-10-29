-module(fixture_call_keyword_case_dotted_member_erlang_call).
-export([x/0]).
'thing.Before'(_) -> ok.
x() ->
    'thing.Before'(1).
