with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    procedure Consume_Widget (Count : A_Val) is begin null; end Consume_Widget;
    my_data : A_Val := Make_Widget(count => AInt (0));
begin
    Consume_Widget(count => my_data);
    my_data := Make_Widget(count => AInt (1));
    Consume_Widget(count => my_data);
end Main;
