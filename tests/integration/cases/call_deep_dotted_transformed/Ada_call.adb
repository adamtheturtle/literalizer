with A_Stub; use A_Stub;
procedure Main is
    type ClientType_ is tagged null record;
    function Fetch (Self : ClientType_; Payload : A_Val) return A_Val is (ANull);
    type AppType_ is tagged record Client : ClientType_; end record;
    App : AppType_;
    procedure Emit (_Arg : A_Val) is begin null; end Emit;
begin
    emit(app.client.fetch(payload => "hello"));
    emit(app.client.fetch(payload => 42));
    emit(app.client.fetch(payload => ABool (True)));
end Main;
