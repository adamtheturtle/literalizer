-module(fixture_literalize_ref_external_declaration_erlang_ref_default).
-export([x/0]).
x() ->
    Shared = [
        1,
        2
    ],
    My_data = Shared.
