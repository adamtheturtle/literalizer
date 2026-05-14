pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("my-key", GStr("value1")),
    #("another-key", GStr("value2")),
    #("normal_key", GStr("value3")),
  ])
  let my_data = GDict([
    #("my-key", GStr("value1")),
    #("another-key", GStr("value2")),
    #("normal_key", GStr("value3")),
  ])
  let _ = my_data
}
