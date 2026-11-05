@discardableResult func process(value: Any = 0) -> Any { 0 }
class _tracerType { @discardableResult func emit(_ _arg: Any = 0) -> Any { 0 } }
let tracer = _tracerType()
tracer.emit(process(value: "hello"));
tracer.emit(process(value: 42));
tracer.emit(process(value: true));
