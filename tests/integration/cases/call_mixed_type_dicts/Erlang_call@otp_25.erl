-module(fixture_call_mixed_type_dicts_erlang_call).
-export([x/0]).
'app.mgr.run'(_) -> ok.
x() ->
    'app.mgr.run'(#{"type" => "create", "pr_id" => "pr_1", "draft" => true}),
    'app.mgr.run'(#{"type" => "create", "pr_id" => "pr_2"}).
