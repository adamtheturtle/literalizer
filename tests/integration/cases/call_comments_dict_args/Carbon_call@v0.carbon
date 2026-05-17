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
fn process(value: CVal) {}
fn Run() {
  // Test cases
  process(CVal.Map(({.key = "type", .val = CVal.Str("create")}, {.key = "pr_id", .val = CVal.Str("pr_1")})));  // first case
  process(CVal.Map(({.key = "type", .val = CVal.Str("update")}, {.key = "pr_id", .val = CVal.Str("pr_2")})));  // second case
  // third case
  process(CVal.Map(({.key = "type", .val = CVal.Str("delete")}, {.key = "pr_id", .val = CVal.Str("pr_3")})));
}
