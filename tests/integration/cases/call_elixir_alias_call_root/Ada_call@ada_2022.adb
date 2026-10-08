with A_Stub; use A_Stub;
procedure Main is
    procedure New (X : A_Val) is begin null; end New;
begin
    New(x => AInt (1));
    New(x => AInt (2));
end Main;
