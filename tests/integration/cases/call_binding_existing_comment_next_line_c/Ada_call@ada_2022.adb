with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    my_data : A_Val := Make_Widget(count => AInt (42));
    my_data := Make_Widget(count => my_data)
    // note;
begin
    Make_Widget(count => my_data);
end Main;
