-module(fixture_sibling_list_values_same_shape_erlang_json_type_otp_json).
-export([x/0]).
x() ->
    My_data = #{
        <<"test"/utf8>> => [5, [<<"compile"/utf8>>, <<"test"/utf8>>]],
        <<"package"/utf8>> => [7, [<<"link"/utf8>>, <<"test"/utf8>>]]
    },
    My_data.
