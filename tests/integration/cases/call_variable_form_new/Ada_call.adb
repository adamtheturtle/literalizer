with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    result : A_Val := AInt (Make_Widget(count => AInt (42)));
begin
    null;
end Main;
