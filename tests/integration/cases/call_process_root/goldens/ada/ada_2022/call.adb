with A_Stub; use A_Stub;
procedure Main is
    procedure Fetch (Data : A_Val) is begin null; end Fetch;
begin
    Fetch(data => AMap'[AEntry ("data", AStr ("hello"))]);
    Fetch(data => AMap'[AEntry ("data", AInt (42))]);
    Fetch(data => AMap'[AEntry ("data", ABool (True))]);
end Main;
