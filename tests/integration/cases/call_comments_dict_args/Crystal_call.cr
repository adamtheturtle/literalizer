module Fixture_call_comments_dict_args_Crystal_call
extend self
def process(value = nil); 0; end
# Test cases
process(value: {"type" => "create", "pr_id" => "pr_1"});  # first case
process(value: {"type" => "update", "pr_id" => "pr_2"});  # second case
# third case
process(value: {"type" => "delete", "pr_id" => "pr_3"});
end
