with A_Stub; use A_Stub;
procedure Main is
    procedure Do_Thing (X : A_Val) is begin null; end Do_Thing;
begin
    Do_Thing(x_ => AInt (1));
    Do_Thing(x_ => AInt (2));
end Main;
