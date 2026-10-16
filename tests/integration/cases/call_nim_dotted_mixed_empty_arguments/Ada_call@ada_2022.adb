with A_Stub; use A_Stub;
procedure Main is
    function Go (Before : A_Val; Populated : A_Val; After : A_Val) return A_Val is (ANull);
begin
    Go(before => AList'[], populated => AList'[AInt (1)], after => AList'[]);
    Go(before => AList'[AStr ("text")], populated => AList'[AInt (2)], after => AList'[]);
    Go(before => AList'[], populated => AList'[AStr ("text")], after => AList'[]);
    Go(before => AList'[AStr ("text")], populated => AList'[AInt (2)], after => AList'[AInt (3)]);
end Main;
