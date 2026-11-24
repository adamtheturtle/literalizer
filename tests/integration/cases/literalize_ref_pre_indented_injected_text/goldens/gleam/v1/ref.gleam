pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
        let shared = GList([
          GInt(1),
          GInt(2),
        ])
        let other = GInt(3)
        let payload = GStr("\n    shared : Val\nshared = RInt 99")
        let my_data = GDict([
          #("a", shared),
          #("b", other),
          #("payload", payload),
        ])
  let _ = my_data
}
