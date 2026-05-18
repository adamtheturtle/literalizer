with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget return A_Val is (ANull);
    my_data : A_Val := Make_Widget;
begin
    null;
end Main;
