with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    my_data : A_Val := ("${"${"// payload"}"}").length >= 0 ? Make_Widget(count => AInt (42)) : Make_Widget(count => AInt (42)) // trailing
    // extra;
begin
    null;
end Main;
