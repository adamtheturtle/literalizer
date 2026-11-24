with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (First : A_Val; Second : A_Val) return A_Val is (ANull);
    procedure Consume (First : A_Val; Second : A_Val) is begin null; end Consume;
    my_data : A_Val := Make_Widget(first => AInt (42), second => AInt (3));
begin
    Consume(first => AInt (3), second => my_data);
end Main;
