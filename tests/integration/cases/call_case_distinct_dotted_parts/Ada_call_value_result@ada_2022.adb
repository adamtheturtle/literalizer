with A_Stub; use A_Stub;
procedure Main is
    function Bar (X : A_Val) return A_Val is (ANull);
    my_data : A_Val := Bar(x => AList'[AInt (1)]);
begin
    null;
end Main;
