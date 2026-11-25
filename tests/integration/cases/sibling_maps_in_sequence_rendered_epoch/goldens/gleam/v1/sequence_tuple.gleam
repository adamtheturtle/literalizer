pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = #(
    GDict([#("k", GStr("2040-01-01T00:00:00+00:00"))]),
    GDict([#("k", GInt(1))]),
  )
  let _ = my_data
}
