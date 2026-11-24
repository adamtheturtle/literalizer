Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"nested", New Dictionary(Of String, Object) From {{"times", New String() {"1900-01-01T00:00:00+00:00"}}}}},
        New Dictionary(Of String, Object) From {}
    }
End Module
