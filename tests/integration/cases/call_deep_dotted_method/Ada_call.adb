with A_Stub; use A_Stub;
procedure Main is
    type Client_T is tagged null record;
    procedure Post (Self : in out Client_T; Data : A_Val) is begin null; end Post;
    type Api_T is tagged record Client : Client_T; end record;
    type Obj_T is tagged record Api : Api_T; end record;
    Obj : Obj_T;
begin
    obj.api.client.post(data => "hello");
    obj.api.client.post(data => 42);
    obj.api.client.post(data => ABool (True));
end Main;
