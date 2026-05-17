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
    {.key = "morning", .val = CVal.Str("09:30:00")},
    {.key = "afternoon", .val = CVal.Str("14:15:00")},
    {.key = "evening", .val = CVal.Str("23:59:59")},
  ));
  let _: CVal = my_data;
}
