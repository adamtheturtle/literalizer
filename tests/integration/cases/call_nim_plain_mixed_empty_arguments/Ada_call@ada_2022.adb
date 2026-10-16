with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Before : A_Val; Populated : A_Val; After : A_Val) return A_Val is (ANull);
begin
    Make_Widget(before => AList'[], populated => AList'[AInt (1)], after => AList'[]);
    Make_Widget(before => AList'[AStr ("text")], populated => AList'[AInt (2)], after => AList'[]);
    Make_Widget(before => AList'[], populated => AList'[AStr ("text")], after => AList'[]);
    Make_Widget(before => AList'[AStr ("text")], populated => AList'[AInt (2)], after => AList'[AInt (3)]);
end Main;
