with A_Stub; use A_Stub;
procedure Main is
    procedure Member (A : A_Val) is begin null; end Member;
begin
    Member(a => AInt (42));
end Main;
