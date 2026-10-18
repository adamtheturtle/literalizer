pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("nested", GDict([#("times", GList([GInt(-2208988800)]))]))]),
    GDict([]),
  ])
  let _ = my_data
}
