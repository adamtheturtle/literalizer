app.client.fetch = @(varargin) [];
emit = @(varargin) [];
emit(app.client.fetch("hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(true))
