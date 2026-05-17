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
    {.key = "s", .val = CVal.Str("string")},
    {.key = "i", .val = CVal.Int(1)},
    {.key = "f", .val = CVal.Float(1.5)},
    {.key = "b", .val = CVal.Bool(true)},
    {.key = "n", .val = CVal.Nil},
    {.key = "d", .val = CVal.Int(1705276800)},
    {.key = "dt", .val = CVal.Int(1705320000)},
    {.key = "by", .val = CVal.Str("48656c6c6f")},
  ));
  my_data = CVal.Map((
    {.key = "s", .val = CVal.Str("string")},
    {.key = "i", .val = CVal.Int(1)},
    {.key = "f", .val = CVal.Float(1.5)},
    {.key = "b", .val = CVal.Bool(true)},
    {.key = "n", .val = CVal.Nil},
    {.key = "d", .val = CVal.Int(1705276800)},
    {.key = "dt", .val = CVal.Int(1705320000)},
    {.key = "by", .val = CVal.Str("48656c6c6f")},
  ));
  let _: CVal = my_data;
}
