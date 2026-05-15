sub process(*@a, *%kw) {}
class TracerType { method emit(*@a, *%kw) {} }
my $tracer = TracerType.new;
tracer.emit(process('hello'));
tracer.emit(process(42));
tracer.emit(process(True));
