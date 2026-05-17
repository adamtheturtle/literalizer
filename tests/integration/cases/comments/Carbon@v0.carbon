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
  let my_data: CVal = CVal.Map((
    // Server configuration
    {.key = "host", .val = CVal.Str("localhost")},  // default host
    {.key = "port", .val = CVal.Int(8080)},
    // Enable debug mode
    {.key = "debug", .val = CVal.Bool(true)},
  ));
  let _: CVal = my_data;
}
