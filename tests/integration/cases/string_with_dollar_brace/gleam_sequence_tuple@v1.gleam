pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    GStr("prefix ${HOME} suffix"),
    GStr("${interpolated}"),
  )
  let _ = my_data
}
