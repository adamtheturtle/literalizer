sub process {}
sub log {}
sub emit {}
log.emit(process("hello"));
log.emit(process(42));
log.emit(process(1));
