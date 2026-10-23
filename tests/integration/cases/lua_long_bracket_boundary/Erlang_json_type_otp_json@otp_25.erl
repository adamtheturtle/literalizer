-module(fixture_lua_long_bracket_boundary_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"]"/utf8>>,
        <<"a]"/utf8>>,
        <<"a]="/utf8>>,
        <<"a]b"/utf8>>
    ],
    My_data.
