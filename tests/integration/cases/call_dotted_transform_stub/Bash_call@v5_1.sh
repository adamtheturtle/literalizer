process() { :; }
tracer.emit() { :; }
tracer.emit "$(process "hello")"
tracer.emit "$(process 42)"
tracer.emit "$(process true)"
