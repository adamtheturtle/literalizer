with A_Stub; use A_Stub;
procedure Main is
    procedure First_Value (Value : A_Val) is begin null; end First_Value;
begin
    First_Value(value => AInt (1));
end Main;
