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
fn Run() {
  let my_data: CVal = CVal.Arr((
    CVal.Map(({.key = "call", .val = CVal.Str("send")}, {.key = "args", .val = CVal.Arr((CVal.Int(1), CVal.Str("email"), CVal.Str("a@gmail.com"), CVal.Int(100)))})),
    CVal.Map(({.key = "call", .val = CVal.Str("recv")}, {.key = "args", .val = CVal.Arr((CVal.Int(2), CVal.Str("sms"), CVal.Str("b@example.com"), CVal.Int(200)))})),
  ));
  let _: CVal = my_data;
}
