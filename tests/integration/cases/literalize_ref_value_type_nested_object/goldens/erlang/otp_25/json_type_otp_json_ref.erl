-module(fixture_literalize_ref_value_type_nested_object_erlang_json_type_otp_json_ref).
-export([x/0]).
x() ->
    Shared = [
        1,
        2
    ],
    Build = [
        1,
        2
    ],
    Json_object = [
        1,
        2
    ],
    Json_allocator = [
        1,
        2
    ],
    Json_entries = [
        1,
        2
    ],
    Json_entry = [
        1,
        2
    ],
    My_data = #{
        <<"field"/utf8>> => Shared,
        <<"nested"/utf8>> => [Shared, #{}],
        <<"build"/utf8>> => Build,
        <<"json_object"/utf8>> => Json_object,
        <<"json_allocator"/utf8>> => Json_allocator,
        <<"json_entries"/utf8>> => Json_entries,
        <<"json_entry"/utf8>> => Json_entry
    },
    My_data.
