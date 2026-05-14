Imports System.Collections.Generic
Module Check
    Dim Deep = New Dictionary(Of String, Object) From {
        {"_", "_"}
    }
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", New Dictionary(Of String, Object) From {{"b", New Dictionary(Of String, Object) From {{"c", Deep}}}}}
    }
End Module
