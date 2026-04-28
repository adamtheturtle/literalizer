with A_Stub; use A_Stub;
procedure Main is
    type Client_T is tagged null record;
    function Fetch (Self : Client_T; Payload : A_Val) return A_Val is (ANull);
    type App_T is tagged record Client : Client_T; end record;
    App : App_T;
    procedure Emit (Arg : A_Val) is begin null; end Emit;
begin
    emit(app.client.fetch(payload => "hello"));
    emit(app.client.fetch(payload => 42));
    emit(app.client.fetch(payload => ABool (True)));
end Main;
