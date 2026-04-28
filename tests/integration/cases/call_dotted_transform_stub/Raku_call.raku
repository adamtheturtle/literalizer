sub process(*@a, *%kw) {}
class LogType { method emit(*@a, *%kw) {} }
my $log = LogType.new;
log.emit(process('hello'));
log.emit(process(42));
log.emit(process(True));
