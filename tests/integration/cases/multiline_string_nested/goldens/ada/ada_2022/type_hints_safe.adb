with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("outer", AList'[AList'[AStr ("nested first line" & Character'Val(10) & "  indented" & Character'Val(10) & Character'Val(10) & "nested last line" & Character'Val(10))]])
    ];
begin
    null;
end Main;
