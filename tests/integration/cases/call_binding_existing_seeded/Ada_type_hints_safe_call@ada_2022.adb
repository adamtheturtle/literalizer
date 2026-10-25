with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    my_data : A_Val := Make_Widget(count => AInt (42));
begin
    declare
        Discarded_Value : constant A_Val := Make_Widget(count => my_data);
        pragma Unreferenced (Discarded_Value);
    begin
        null;
    end;
    my_data := Make_Widget(count => my_data);
    declare
        Discarded_Value : constant A_Val := Make_Widget(count => my_data);
        pragma Unreferenced (Discarded_Value);
    begin
        null;
    end;
end Main;
