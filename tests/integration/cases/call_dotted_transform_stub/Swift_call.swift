@discardableResult func process(value: Any = 0) -> Any { 0 }
class _logType { @discardableResult func emit(_ _arg: Any = 0) -> Any { 0 } }
let log = _logType()
log.emit(process(value: "hello"));
log.emit(process(value: 42));
log.emit(process(value: true));
