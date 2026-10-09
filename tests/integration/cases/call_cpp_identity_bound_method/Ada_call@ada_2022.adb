with A_Stub; use A_Stub;
procedure Main is
    function Go (Value : A_Val) return A_Val is (ANull);
    item : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
begin
    Go(value => item);
end Main;
