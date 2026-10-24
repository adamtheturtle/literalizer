with A_Stub; use A_Stub;
procedure Main is
    procedure Make_Widget (Before : A_Val) is begin null; end Make_Widget;
begin
    Make_Widget(Before => AInt (1));
end Main;
