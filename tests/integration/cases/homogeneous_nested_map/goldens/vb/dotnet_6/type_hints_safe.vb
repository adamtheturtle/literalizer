Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"first", New Dictionary(Of String, Object) From {{"x", 1}, {"y", 2}}},
        {"second", New Dictionary(Of String, Object) From {{"z", 3}}}
    }
End Module
