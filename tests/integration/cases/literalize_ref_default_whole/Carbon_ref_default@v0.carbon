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
  let my_var: CVal = CVal.Map((
    {.key = "_", .val = CVal.Str("_")},
  ));
  let my_data: CVal = my_var;
  let _: CVal = my_data;
}
