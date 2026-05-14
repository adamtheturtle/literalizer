pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("level1", GDict([#("level2", GDict([#("level3", GDict([#("level4", GDict([#("value", GStr("deep")), #("items", GList([GStr("a"), GStr("b")]))]))])), #("sibling", GInt(42))])), #("tags", GList([GDict([#("name", GStr("tag1")), #("meta", GDict([#("priority", GInt(1)), #("labels", GList([GStr("x"), GStr("y")]))]))])]))])),
  ])
  let my_data = GDict([
    #("level1", GDict([#("level2", GDict([#("level3", GDict([#("level4", GDict([#("value", GStr("deep")), #("items", GList([GStr("a"), GStr("b")]))]))])), #("sibling", GInt(42))])), #("tags", GList([GDict([#("name", GStr("tag1")), #("meta", GDict([#("priority", GInt(1)), #("labels", GList([GStr("x"), GStr("y")]))]))])]))])),
  ])
  let _ = my_data
}
