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

pub fn main() {
  app_client_fetch(GStr("hello"))
  app_client_fetch(GInt(42))
  app_client_fetch(GBool(True))
}
