with A_Stub; use A_Stub;
procedure Main is
    procedure Consume (Value : A_Val) is begin null; end Consume;
begin
    Consume(value => AInt (-2147483649));
    Consume(value => AInt (2147483648));
end Main;
