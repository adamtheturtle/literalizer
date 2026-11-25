with A_Stub; use A_Stub;
procedure Main is
    function Go (Value : A_Val) return A_Val is (ANull);
    my_data : A_Val := Go(value => AList'[]);
begin
    null;
end Main;
