api.worker.process = @(varargin) [];
api.worker.process({1, struct()}, 42)
api.worker.process({2, struct('x', "s")}, 43)
