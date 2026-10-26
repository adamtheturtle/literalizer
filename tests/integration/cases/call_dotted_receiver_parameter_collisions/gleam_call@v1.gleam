pub type GVal {
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn api_worker_process(_self: a, _self_: b) -> Nil { Nil }

pub fn main() {
  let _ = api_worker_process(GDict([]), GDict([]))
}
