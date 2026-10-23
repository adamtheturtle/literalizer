Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"date", New DateOnly(99, 5, 27)},
        {"naive", "0001-01-01T12:30:00"},
        {"recent", "2024-05-27T10:00:00"}
    }
End Module
