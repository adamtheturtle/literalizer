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
class ClientType_ { fn post[self: Self](data: CVal) {} }
class ApiType_ { var client: ClientType_; }
class ObjType_ { var api: ApiType_; }
var obj: ObjType_;
fn Run() {
  obj.api.client.post(CVal.Str("hello"));
  obj.api.client.post(CVal.Int(42));
  obj.api.client.post(CVal.Bool(true));
}
