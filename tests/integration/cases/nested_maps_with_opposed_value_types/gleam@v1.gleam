pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("input", GDict([#("name", GStr("alice")), #("city", GStr("paris"))])), #("expected", GDict([#("count", GInt(1)), #("total", GInt(2))]))]),
    GDict([#("input", GDict([#("name", GInt(10)), #("city", GInt(20))])), #("expected", GDict([#("count", GStr("done")), #("total", GStr("pending"))]))]),
  ])
  let _ = my_data
}
