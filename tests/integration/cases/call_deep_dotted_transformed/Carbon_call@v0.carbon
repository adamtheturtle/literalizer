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
class ClientType_ { fn fetch[self: Self](payload: CVal) {} }
class AppType_ { var client: ClientType_; }
var app: AppType_;
fn emit(_arg: CVal) {}
fn Run() {
  emit(app.client.fetch(CVal.Str("hello")));
  emit(app.client.fetch(CVal.Int(42)));
  emit(app.client.fetch(CVal.Bool(true)));
}
