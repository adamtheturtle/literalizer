with A_Stub; use A_Stub;
procedure Main is
    procedure Dothing (X : A_Val) is begin null; end Dothing;
begin
    Dothing(x => AInt (1));
    Dothing(x => AInt (2));
end Main;
