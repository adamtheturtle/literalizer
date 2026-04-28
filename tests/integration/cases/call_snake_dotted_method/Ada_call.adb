with A_Stub; use A_Stub;
procedure Main is
    type Http_Client_T is tagged null record;
    procedure Fetch (Self : in out Http_Client_T; Payload : A_Val) is begin null; end Fetch;
    type My_App_T is tagged record Http_Client : Http_Client_T; end record;
    My_App : My_App_T;
begin
    my_app.http_client.fetch(payload => "hello");
    my_app.http_client.fetch(payload => 42);
    my_app.http_client.fetch(payload => ABool (True));
end Main;
