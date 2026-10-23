-module(fixture_string_with_hash_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"issue #{42}"/utf8>>,
        <<"color #red"/utf8>>
    ],
    My_data.
