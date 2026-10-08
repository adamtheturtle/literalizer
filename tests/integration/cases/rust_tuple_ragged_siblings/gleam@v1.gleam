pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GStr("set_task"), GStr("web"), GStr("lint_web")]),
    GList([GStr("merge_pipelines")]),
  ])
  let _ = my_data
}
