with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Value : A_Val) return A_Val is (ANull);
    items : A_Val := AList'[];
begin
    Make_Widget(value => items);
end Main;
