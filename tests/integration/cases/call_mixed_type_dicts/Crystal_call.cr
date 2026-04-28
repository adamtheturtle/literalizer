module Fixture_call_mixed_type_dicts_Crystal_call
extend self
class MgrType_; def op(operation = nil); 0; end; end
class AppType_; def mgr; MgrType_.new; end; end
app = AppType_.new
app.mgr.op(operation: {"type" => "create", "pr_id" => "pr_1", "draft" => true});
app.mgr.op(operation: {"type" => "create", "pr_id" => "pr_2"});
end
