with A_Stub; use A_Stub;
procedure Main is
    type Http_ClientType_ is tagged null record;
    procedure Fetch (Self : in out Http_ClientType_; Payload : A_Val) is begin null; end Fetch;
    type My_AppType_ is tagged record Http_Client : Http_ClientType_; end record;
    My_App : My_AppType_;
begin
    my_app.http_client.fetch(payload => "hello");
    my_app.http_client.fetch(payload => 42);
    my_app.http_client.fetch(payload => ABool (True));
end Main;
