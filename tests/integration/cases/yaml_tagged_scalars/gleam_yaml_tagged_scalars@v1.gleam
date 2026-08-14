pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("explicit_string", GStr("5")),
    #("six", GStr("explicitly tagged key")),
  ])
  let _ = my_data
}
