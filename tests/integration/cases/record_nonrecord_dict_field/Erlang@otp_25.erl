-module(fixture_record_nonrecord_dict_field_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "label" => "tag",
        "meta" => #{}
    },
    My_data.
