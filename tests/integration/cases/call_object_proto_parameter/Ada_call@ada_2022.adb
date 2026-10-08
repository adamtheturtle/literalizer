with A_Stub; use A_Stub;
procedure Main is
    procedure Capture (Proto : A_Val) is begin null; end Capture;
begin
    Capture(__proto__ => AInt (1));
end Main;
