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
    {.key = "host", .val = CVal.Str("it's here")},  // a comment
    {.key = "port", .val = CVal.Int(80)},  // another
  ));
  my_data = CVal.Map((
    {.key = "host", .val = CVal.Str("it's here")},  // a comment
    {.key = "port", .val = CVal.Int(80)},  // another
  ));
  let _: CVal = my_data;
}
