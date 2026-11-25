with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
begin
    Process(value => AMap'[AEntry ("value", AInt (1))]);
    Process(value => AMap'[AEntry ("value", AStr ("hello"))]);
end Main;
