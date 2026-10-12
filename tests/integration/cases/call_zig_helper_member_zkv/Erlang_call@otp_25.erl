-module(fixture_call_zig_helper_member_zkv_erlang_call).
-export([x/0]).
'obj.ZKV'(_) -> ok.
x() ->
    'obj.ZKV'(1).
