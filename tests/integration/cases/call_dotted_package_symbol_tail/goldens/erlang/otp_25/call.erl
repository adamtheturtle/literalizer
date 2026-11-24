-module(fixture_call_dotted_package_symbol_tail_erlang_call).
-export([x/0]).
'helper.list'(_) -> ok.
x() ->
    'helper.list'(1).
