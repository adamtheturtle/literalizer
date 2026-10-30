with A_Stub; use A_Stub;
procedure Main is
    procedure Bar (X : A_Val) is begin null; end Bar;
begin
    Bar(x => AList'[AInt (1)]);
end Main;
