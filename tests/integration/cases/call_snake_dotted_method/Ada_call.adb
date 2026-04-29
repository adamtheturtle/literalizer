with A_Stub; use A_Stub;
procedure Main is
    procedure Fetch (Payload : A_Val) is begin null; end Fetch;
begin
    Fetch(payload => AStr ("hello"));
    Fetch(payload => AInt (42));
    Fetch(payload => ABool (True));
end Main;
