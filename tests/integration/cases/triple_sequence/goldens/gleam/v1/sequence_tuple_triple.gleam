pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    GInt(1),
    GStr("hello"),
    GBool(True),
  )
  let _ = my_data
}
