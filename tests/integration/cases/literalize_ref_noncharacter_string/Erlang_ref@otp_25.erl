-module(fixture_literalize_ref_noncharacter_string_erlang_ref).
-export([x/0]).
x() ->
    Source_value = [65534, 65535],
    My_data = Source_value,
    My_data.
