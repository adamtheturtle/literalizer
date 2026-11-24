Imports System.Collections.Generic
Module Check
    ' first dotted key
    ' second dotted key
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {{"b", 1}, {"c", 2}}}
    }
End Module
