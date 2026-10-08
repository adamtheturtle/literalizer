pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    #(GStr("set_task"), GStr("web"), GStr("lint_web")),
    #(GStr("merge_pipelines")),
  )
  let _ = my_data
}
