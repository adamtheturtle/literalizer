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
class MgrType_ { fn run[self: Self](operation: CVal) {} }
class AppType_ { var mgr: MgrType_; }
var app: AppType_;
fn Run() {
  app.mgr.run(CVal.Map(({.key = "type", .val = CVal.Str("create")}, {.key = "pr_id", .val = CVal.Str("pr_1")}, {.key = "draft", .val = CVal.Bool(true)})));
  app.mgr.run(CVal.Map(({.key = "type", .val = CVal.Str("create")}, {.key = "pr_id", .val = CVal.Str("pr_2")})));
}
