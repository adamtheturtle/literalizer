with A_Stub; use A_Stub;
procedure Main is
    type ClientType_ is tagged null record;
    procedure Fetch (Self : in out ClientType_; Payload : A_Val) is begin null; end Fetch;
    type AppType_ is tagged record Client : ClientType_; end record;
    App : AppType_;
begin
    app.client.fetch(payload => "hello");
    app.client.fetch(payload => 42);
    app.client.fetch(payload => ABool (True));
end Main;
