def process(Map _args) { null }
class _LogType { def emit(Map _args) { null } }
def log = new _LogType()
log.emit(process(value: "hello"))
log.emit(process(value: 42))
log.emit(process(value: true))
