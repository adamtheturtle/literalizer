with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Value : A_Val) return A_Val is (ANull);
    my_data : A_Val := Make_Widget(value => AList'[]);
begin
    null;
end Main;
