with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    my_data : A_Val := (`__LINE__ > 0) ? Make_Widget(count => AInt (42)) : Make_Widget(count => AInt (42)) // trailing `marker;
begin
    null;
end Main;
