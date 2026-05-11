pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([GDict([#("name", GStr("Alice"))]), GDict([#("name", GStr("Bob"))])]),
    GList([GDict([#("name", GStr("Charlie"))]), GDict([#("name", GStr("Dave"))])]),
  ])
  let my_data = GList([
    GList([GDict([#("name", GStr("Alice"))]), GDict([#("name", GStr("Bob"))])]),
    GList([GDict([#("name", GStr("Charlie"))]), GDict([#("name", GStr("Dave"))])]),
  ])
  let _ = my_data
}
