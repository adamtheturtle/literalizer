with A_Stub; use A_Stub;
procedure Main is
    procedure Make_Widget (First_Value : A_Val; Second_Value : A_Val) is begin null; end Make_Widget;
begin
    Make_Widget(first_value => AList'[AInt (1)], second_value => AList'[AStr ("text")]);
end Main;
