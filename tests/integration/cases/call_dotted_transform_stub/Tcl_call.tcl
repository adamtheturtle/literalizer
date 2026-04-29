proc process {args} {return {}}
proc tracer.emit {args} {}
tracer.emit [process "hello"]
tracer.emit [process 42]
tracer.emit [process 1]
