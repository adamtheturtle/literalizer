sub process {}
sub tracer {}
sub emit {}
tracer.emit(process("hello"));
tracer.emit(process(42));
tracer.emit(process(1));
