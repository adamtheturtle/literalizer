with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Value : A_Val) return A_Val is (ANull);
    procedure Consume (Value : A_Val) is begin null; end Consume;
    my_data : A_Val := Make_Widget(value => AInt (42));
begin
    Consume(value => my_data);
end Main;
