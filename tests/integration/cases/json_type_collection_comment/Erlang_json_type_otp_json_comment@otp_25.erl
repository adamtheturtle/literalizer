-module(fixture_json_type_collection_comment_erlang_json_type_otp_json_comment).
-export([x/0]).
x() ->
    My_data = #{
        <<"a"/utf8>> => 1,  % About a.
        <<"b"/utf8>> => 2
    },
    My_data.
