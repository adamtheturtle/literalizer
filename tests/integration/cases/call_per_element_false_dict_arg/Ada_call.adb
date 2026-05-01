with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
begin
    Process(value => AMap'[AEntry ("a", AInt (1)), AEntry ("b", AStr ("x"))]);
end Main;
