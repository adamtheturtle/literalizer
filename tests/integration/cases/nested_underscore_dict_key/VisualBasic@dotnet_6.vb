Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"outer", New Object() {New Dictionary(Of String, Object) From {{"_", 1}}}}
    }
End Module
