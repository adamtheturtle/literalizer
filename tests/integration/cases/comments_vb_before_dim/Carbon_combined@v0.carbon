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
  var my_data: CVal = CVal.Map((
    // Configuration
    {.key = "name", .val = CVal.Str("app")},
    // Port setting
    {.key = "port", .val = CVal.Int(3000)},
  ));
  my_data = CVal.Map((
    // Configuration
    {.key = "name", .val = CVal.Str("app")},
    // Port setting
    {.key = "port", .val = CVal.Int(3000)},
  ));
  let _: CVal = my_data;
}
