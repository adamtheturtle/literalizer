choice CVal {
  Nil,
  Bool(bool),
  Int(i64),
  UInt(u64),
  Float(f64),
  Str(Core.String),
  Arr(Core.Array(CVal)),
  Map(Core.Array({.key: Core.String, .val: CVal})),
  Set(Core.Array(CVal)),
}
fn process(value: CVal) {}
class TracerType_ { fn emit[self: Self](_arg: CVal) {} }
var tracer: TracerType_;
fn Run() {
  tracer.emit(process(CVal.Str("hello")));
  tracer.emit(process(CVal.Int(42)));
  tracer.emit(process(CVal.Bool(true)));
}
