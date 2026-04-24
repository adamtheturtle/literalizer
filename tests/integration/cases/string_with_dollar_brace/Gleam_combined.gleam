pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("prefix ${HOME} suffix"),
    GStr("${interpolated}"),
  ])
  let my_data = GList([
    GStr("prefix ${HOME} suffix"),
    GStr("${interpolated}"),
  ])
  let _ = my_data
}
