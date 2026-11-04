with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    procedure Consume (Count : A_Val) is begin null; end Consume;
    my_data : A_Val := Make_Widget(count => ANull);
begin
    Consume(count => my_data);
    my_data := Make_Widget(count => AInt (42));
    Consume(count => my_data);
end Main;
