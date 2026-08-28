Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"p", New Dictionary(Of String, Object) From {{"a", 1}}},
        {"q", New Dictionary(Of String, Object) From {{"a", 1099511627776}}}
    }
End Module
