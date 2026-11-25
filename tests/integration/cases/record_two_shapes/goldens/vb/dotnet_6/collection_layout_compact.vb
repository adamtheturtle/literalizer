Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"metrics", New Dictionary(Of String, Object) From {{"count", 100}, {"rate", 50}}},
        {"flags", New Dictionary(Of String, Object) From {{"retries", 3}, {"timeout", 30}}}
    }
End Module
