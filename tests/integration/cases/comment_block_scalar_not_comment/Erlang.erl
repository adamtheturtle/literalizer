-module(check).
-export([x/0]).
x() ->
    My_data = #{
    "description" => "# not a comment\n",
    "name" => "foo"
},
    My_data.
