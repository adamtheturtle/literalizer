with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    my_data : A_Val := Make_Widget(count => AInt (0));
begin
    my_data := Make_Widget(count => AInt (1));
end Main;
