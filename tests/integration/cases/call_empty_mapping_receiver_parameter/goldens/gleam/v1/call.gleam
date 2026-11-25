pub type GVal {
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn api_process(_self: a) -> Nil { Nil }

pub fn main() {
  let _ = api_process(GDict([]))
}
