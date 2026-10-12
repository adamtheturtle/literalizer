with A_Stub; use A_Stub;
procedure Main is
    procedure Class (A : A_Val) is begin null; end Class;
begin
    Class(a => AInt (42));
end Main;
