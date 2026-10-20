with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Text : A_Val) return A_Val is (ANull);
    my_data : A_Val := Make_Widget(text => AStr ("text"));
begin
    null;
end Main;
