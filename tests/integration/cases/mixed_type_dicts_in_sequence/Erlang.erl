-module(check).
-export([x/0]).
x() ->
    My_data = [
        #{"type" => "create", "pr_id" => "pr_1", "draft" => true},
        #{"type" => "create", "pr_id" => "pr_2"}
    ],
    My_data.
