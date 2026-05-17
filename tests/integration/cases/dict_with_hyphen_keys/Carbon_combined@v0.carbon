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
    {.key = "my-key", .val = CVal.Str("value1")},
    {.key = "another-key", .val = CVal.Str("value2")},
    {.key = "normal_key", .val = CVal.Str("value3")},
  ));
  my_data = CVal.Map((
    {.key = "my-key", .val = CVal.Str("value1")},
    {.key = "another-key", .val = CVal.Str("value2")},
    {.key = "normal_key", .val = CVal.Str("value3")},
  ));
  let _: CVal = my_data;
}
