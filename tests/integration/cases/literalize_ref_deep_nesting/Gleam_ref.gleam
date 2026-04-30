pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let deep = GDict([
    #("_", GStr("_")),
  ])
  let my_data = GDict([
    #("a", GDict([#("b", GDict([#("c", deep)]))])),
  ])
  let _ = my_data
}
