with A_Stub; use A_Stub;
procedure Main is
    procedure Consume (Value : A_Val) is begin null; end Consume;
    item : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
begin
    Consume(value => item);
end Main;
