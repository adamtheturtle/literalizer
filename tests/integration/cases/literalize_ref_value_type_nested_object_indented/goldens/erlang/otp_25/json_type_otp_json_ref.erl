-module(fixture_literalize_ref_value_type_nested_object_indented_erlang_json_type_otp_json_ref).
-export([x/0]).
x() ->
            Shared = [
                1,
                2
            ],
            My_data = #{
                <<"field"/utf8>> => #{<<"nested"/utf8>> => Shared},
                <<"text"/utf8>> => <<"first\n{ \" // }"/utf8>>
            },
    My_data.
