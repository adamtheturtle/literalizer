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
  var my_data: CVal = CVal.Arr((
    CVal.Map(({.key = "type", .val = CVal.Str("create")}, {.key = "pr_id", .val = CVal.Str("pr_1")}, {.key = "draft", .val = CVal.Bool(true)})),
    CVal.Map(({.key = "type", .val = CVal.Str("create")}, {.key = "pr_id", .val = CVal.Str("pr_2")})),
  ));
  my_data = CVal.Arr((
    CVal.Map(({.key = "type", .val = CVal.Str("create")}, {.key = "pr_id", .val = CVal.Str("pr_1")}, {.key = "draft", .val = CVal.Bool(true)})),
    CVal.Map(({.key = "type", .val = CVal.Str("create")}, {.key = "pr_id", .val = CVal.Str("pr_2")})),
  ));
  let _: CVal = my_data;
}
