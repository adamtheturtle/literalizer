Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"quote""backslash\", 1},
        {"line" & Chr(10) & "break", 2},
        {"$(literal)${text}", 3},
        {"RStr prefix", 4}
    }
End Module
