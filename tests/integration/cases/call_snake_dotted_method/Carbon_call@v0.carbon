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
class Http_ClientType_ { fn fetch[self: Self](payload: CVal) {} }
class My_AppType_ { var http_client: Http_ClientType_; }
var my_app: My_AppType_;
fn Run() {
  my_app.http_client.fetch(CVal.Str("hello"));
  my_app.http_client.fetch(CVal.Int(42));
  my_app.http_client.fetch(CVal.Bool(true));
}
