-module(fixture_string_escaped_quotes_and_dashes_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = <<"hello \"world\" -- not a comment"/utf8>>,
    My_data.
