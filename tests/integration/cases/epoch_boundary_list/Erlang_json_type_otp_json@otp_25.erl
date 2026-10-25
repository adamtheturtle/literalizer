-module(fixture_epoch_boundary_list_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = [
        <<"1901-12-13T20:45:51"/utf8>>,
        <<"1901-12-13T20:45:52"/utf8>>,
        <<"2038-01-19T03:14:07"/utf8>>,
        <<"2038-01-19T03:14:08"/utf8>>
    ],
    My_data.
