with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Text : A_Val) return A_Val is (ANull);
    my_data : A_Val := Make_Widget(text => AStr ("first ""quote""" & Character'Val(10) & "// string body")) // note
    // extra;
begin
    null;
end Main;
