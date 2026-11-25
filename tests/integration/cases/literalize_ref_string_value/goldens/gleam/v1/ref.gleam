pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let shared = GStr("s")
  let my_data = GDict([
    #("value", shared),
  ])
  let _ = my_data
}
