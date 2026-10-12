-module(fixture_call_binding_member_zval_zig_erlang_call).
-export([x/0]).
'obj.ZVal'(_) -> undefined.
x() ->
    My_data = 'obj.ZVal'(42) // note,
    My_data.
