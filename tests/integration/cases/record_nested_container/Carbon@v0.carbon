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
    {.key = "title", .val = CVal.Str("report")},
    {.key = "tags", .val = CVal.Arr((CVal.Str("draft"), CVal.Str("urgent"), CVal.Str("review")))},
    {.key = "priority", .val = CVal.Int(2)},
  ));
  let _: CVal = my_data;
}
