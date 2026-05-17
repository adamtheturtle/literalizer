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
    {.key = "host", .val = CVal.Str("localhost")},
    {.key = "port", .val = CVal.Nil},  // not configured yet
    {.key = "debug", .val = CVal.Bool(true)},
  ));
  my_data = CVal.Map((
    {.key = "host", .val = CVal.Str("localhost")},
    {.key = "port", .val = CVal.Nil},  // not configured yet
    {.key = "debug", .val = CVal.Bool(true)},
  ));
  let _: CVal = my_data;
}
