with A_Stub; use A_Stub;
procedure Main is
    procedure Consume (Value : A_Val) is begin null; end Consume;
    value : A_Val := ANull;
begin
    Consume(value => value);
end Main;
