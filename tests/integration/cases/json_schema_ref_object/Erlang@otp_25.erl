-module(fixture_json_schema_ref_object_erlang).
-export([x/0]).
x() ->
    My_data = #{
        "schema" => #{"$ref" => "#/defs/Foo"}
    },
    My_data.
