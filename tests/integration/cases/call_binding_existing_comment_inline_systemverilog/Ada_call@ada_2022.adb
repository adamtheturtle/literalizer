with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    my_data : A_Val := AInt (42);
begin
    my_data := Make_Widget(count => AInt (42)) // note;
end Main;
