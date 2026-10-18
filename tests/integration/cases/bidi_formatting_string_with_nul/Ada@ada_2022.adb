with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("v", AStr ("a‪" & Character'Val(0) & "é😀b"))
    ];
begin
    null;
end Main;
