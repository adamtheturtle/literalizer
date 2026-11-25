-module(fixture_multiline_string_scalar_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = <<"\nroot first line\n  indented\n\nroot last line\n"/utf8>>,
    My_data.
