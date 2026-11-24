pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn app_client_fetch(_payload: a) -> Nil { Nil }
pub fn emit(__arg: a) -> Nil { Nil }

pub fn main() {
  let _ = emit(app_client_fetch(GStr("hello")))
  let _ = emit(app_client_fetch(GInt(42)))
  let _ = emit(app_client_fetch(GBool(True)))
}
