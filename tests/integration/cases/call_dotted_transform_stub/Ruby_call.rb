def process(*a); end
class LogType; def emit(*a, **kw); end; end
log = LogType.new
log.emit(process(value: "hello"))
log.emit(process(value: 42))
log.emit(process(value: true))
