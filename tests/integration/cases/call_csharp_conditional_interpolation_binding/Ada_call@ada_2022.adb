with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Count : A_Val) return A_Val is (ANull);
    my_data : A_Val := $"{(true ? "// payload" : "ok")}" // trailing
    // extra;
begin
    null;
end Main;
