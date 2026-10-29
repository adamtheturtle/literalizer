with A_Stub; use A_Stub;
procedure Main is
    procedure Before (Value : A_Val) is begin null; end Before;
begin
    Before(value => AInt (1));
end Main;
