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
  let val_x: CVal = CVal.Map((
    {.key = "_", .val = CVal.Str("_")},
  ));
  let val_y: CVal = CVal.Map((
    {.key = "_", .val = CVal.Str("_")},
  ));
  let my_data: CVal = CVal.Arr((
    val_x,
    val_y,
  ));
  let _: CVal = my_data;
}
