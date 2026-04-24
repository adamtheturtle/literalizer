pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
}
pub fn app_client_fetch(_payload: a) -> Nil { panic }
pub fn emit(__arg: a) -> Nil { panic }

pub fn main() {
  emit(app_client_fetch(GStr("hello")))
  emit(app_client_fetch(GInt(42)))
  emit(app_client_fetch(GBool(True)))
}
