-module(fixture_sequence_ragged_siblings_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        [<<"set_task"/utf8>>, <<"web"/utf8>>, <<"lint_web"/utf8>>],
        [<<"merge_pipelines"/utf8>>]
    ],
    My_data.
