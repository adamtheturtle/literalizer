with A_Stub; use A_Stub;
procedure Main is
    procedure Make_Widget (Value : A_Val) is begin null; end Make_Widget;
    value : A_Val := AInt (1);
begin
    Make_Widget(value => value);
end Main;
