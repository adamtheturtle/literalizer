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
class ThrottlerType_ { fn check[self: Self](user_id: CVal, ts: CVal) {} }
var throttler: ThrottlerType_;
fn emit(_arg: CVal) {}
fn Run() {
  emit(throttler.check(CVal.Str("user_1"), CVal.Float(1000.0)));
  emit(throttler.check(CVal.Str("user_2"), CVal.Float(2000.5)));
}
