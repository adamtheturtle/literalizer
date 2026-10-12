with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Items : A_Val) return A_Val is (ANull);
    my_data : A_Val := Make_Widget(items => AList'[AList'[AInt (1), AInt (2)], AList'[AInt (3)]]);
begin
    null;
end Main;
