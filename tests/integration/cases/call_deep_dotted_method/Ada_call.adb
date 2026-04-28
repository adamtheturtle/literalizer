with A_Stub; use A_Stub;
procedure Main is
    type ClientType_ is tagged null record;
    procedure Post (Self : in out ClientType_; Data : A_Val) is begin null; end Post;
    type ApiType_ is tagged record Client : ClientType_; end record;
    type ObjType_ is tagged record Api : ApiType_; end record;
    Obj : ObjType_;
begin
    obj.api.client.post(data => "hello");
    obj.api.client.post(data => 42);
    obj.api.client.post(data => ABool (True));
end Main;
