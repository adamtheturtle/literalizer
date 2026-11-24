with A_Stub; use A_Stub;
procedure Main is
    function Record_Entry (S : A_Val; N : A_Val; B : A_Val) return A_Val is (ANull);
    my_data : A_Val := Record_Entry(s => AStr ("a"), n => AInt (1), b => ABool (True));
begin
    null;
end Main;
