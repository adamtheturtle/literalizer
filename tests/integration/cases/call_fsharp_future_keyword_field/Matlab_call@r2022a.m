app.process.fetch = @(varargin) [];
app.process.fetch(struct('data', "hello"))
app.process.fetch(struct('data', 42))
app.process.fetch(struct('data', true))
