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
    CVal.Str("2024-01-15T12:30:00.123456+00:00"),
    CVal.Str("2024-06-01T08:00:00+00:00"),
  ));
  let _: CVal = my_data;
}
