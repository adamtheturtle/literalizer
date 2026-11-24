Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"date", New DateOnly(99, 5, 27)},
        {"naive", -62135551800},
        {"recent", 1716804000}
    }
End Module
