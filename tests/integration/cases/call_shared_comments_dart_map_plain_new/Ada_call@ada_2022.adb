with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    my_data : A_Val := ("${{'value': '// payload'}['value']}").length >= 0 ? Make_Widget(count => AInt (42)) : Make_Widget(count => AInt (42));
begin
    null;
end Main;
