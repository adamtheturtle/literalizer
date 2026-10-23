pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    GStr("issue #{42}"),
    GStr("color #red"),
  )
  let _ = my_data
}
