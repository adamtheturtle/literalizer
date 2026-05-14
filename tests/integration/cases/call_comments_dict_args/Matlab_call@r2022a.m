process = @(varargin) [];
% Test cases
process(struct('type', "create", 'pr_id', "pr_1"))  % first case
process(struct('type', "update", 'pr_id', "pr_2"))  % second case
% third case
process(struct('type', "delete", 'pr_id', "pr_3"))
