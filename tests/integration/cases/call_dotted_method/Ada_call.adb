with A_Stub; use A_Stub;
procedure Main is
    type Client_T is tagged null record;
    procedure Fetch (Self : in out Client_T; Payload : A_Val) is begin null; end Fetch;
    type App_T is tagged record Client : Client_T; end record;
    App : App_T;
begin
    app.client.fetch(payload => "hello");
    app.client.fetch(payload => 42);
    app.client.fetch(payload => ABool (True));
end Main;
