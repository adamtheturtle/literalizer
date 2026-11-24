process.api.fetch = @(varargin) [];
process.api.fetch(struct('data', "hello"))
process.api.fetch(struct('data', 42))
process.api.fetch(struct('data', true))
