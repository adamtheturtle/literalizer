with A_Stub; use A_Stub;
procedure Main is
    procedure Consume (Value : A_Val) is begin null; end Consume;
    shared : A_Val := AInt (42);
begin
    Consume(value => shared);
end Main;
