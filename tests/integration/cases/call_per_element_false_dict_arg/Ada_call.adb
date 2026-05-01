with A_Stub; use A_Stub;
procedure Main is
    procedure Send (Value : A_Val) is begin null; end Send;
begin
    Send(value => AMap'[AEntry ("a", AInt (1)), AEntry ("b", AStr ("x"))]);
end Main;
