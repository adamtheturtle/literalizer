with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    procedure Make_Widget (Count : A_Val) is begin null; end Make_Widget;
    my_data : A_Val := Make_Widget(count => AInt (42));
    Make_Widget(count => my_data);
begin
    my_data := Make_Widget(count => my_data);
    Make_Widget(count => my_data);
end Main;
