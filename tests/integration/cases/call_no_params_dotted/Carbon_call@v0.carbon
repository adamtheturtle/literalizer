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
class ThrottlerType_ { fn check[self: Self]() {} }
var throttler: ThrottlerType_;
fn Run() {
  throttler.check();
  throttler.check();
}
