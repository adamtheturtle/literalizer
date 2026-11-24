with A_Stub; use A_Stub;
procedure Main is
    procedure Consume (Value : A_Val) is begin null; end Consume;
    my_null : A_Val := ANull;
    regular_null : A_Val := ANull;
begin
    Consume(value => my_null);
    Consume(value => regular_null);
end Main;
