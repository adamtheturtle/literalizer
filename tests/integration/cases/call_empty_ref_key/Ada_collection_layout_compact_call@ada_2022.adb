with A_Stub; use A_Stub;
procedure Main is
    procedure Consume (Value : A_Val) is begin null; end Consume;
    external_value : A_Val := AInt (1);
begin
    Consume(value => external_value);
end Main;
