-module(fixture_string_with_backslash_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"C:\\path\\to\\file"/utf8>>,
        <<"back\\\\slash"/utf8>>,
        <<"hello \\\"world\\\""/utf8>>,
        <<"path\\to \"# file"/utf8>>,
        <<"trailing\\"/utf8>>,
        <<"both \"quotes''' here"/utf8>>,
        <<"line1\\nline2\nwith newline"/utf8>>
    ],
    My_data.
