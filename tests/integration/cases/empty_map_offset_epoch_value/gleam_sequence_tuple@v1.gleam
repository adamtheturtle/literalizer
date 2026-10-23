pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = #(
    GDict([#("timestamp", GStr("2040-01-01T03:00:00+03:00"))]),
    GDict([]),
  )
  let _ = my_data
}
