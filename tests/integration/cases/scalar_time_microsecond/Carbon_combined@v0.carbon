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
    {.key = "exact_millisecond", .val = CVal.Str("09:30:15.123000")},
    {.key = "sub_millisecond", .val = CVal.Str("09:30:15.123456")},
  ));
  my_data = CVal.Map((
    {.key = "exact_millisecond", .val = CVal.Str("09:30:15.123000")},
    {.key = "sub_millisecond", .val = CVal.Str("09:30:15.123456")},
  ));
  let _: CVal = my_data;
}
