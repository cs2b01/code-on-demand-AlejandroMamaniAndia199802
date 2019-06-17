$(function(){
    var url = "http://127.0.0.1:5000/messages";


    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url ,
            insertUrl: url ,
            updateUrl: url ,
            deleteUrl: url ,
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),
        editing: {
            allowUpdating: true,
            allowDeleting: true,
            allowAdding: true
        },
        remoteOperations: {
            sorting: true,
            paging: true
        },
        paging: {
            pageSize: 5
        },
        pager: {
            showPageSizeSelector: true,
            allowedPageSizes: [5, 10, 20]
        },
        headerFilter: {
            visible: true
        },
        filterRow: {
            visible: true
        },

        columns: [{
            dataField: "id",
            dataType: "number",
            allowEditing: false
        }, {
            dataField: "content"
        }, {
            dataField: "sent_on",
            allowEditing: false
        }, {
            dataField: "user_from.name",
            caption: "FROM: ",
            lookup: {
                    dataSource: DevExpress.data.AspNet.createStore({
                        key: "name",
                        loadUrl: "http://127.0.0.1:5000/users",
                        onBeforeSend: function(method, ajaxOptions) {
                            ajaxOptions.xhrFields = { withCredentials: true };
                        }
                    }),
                    displayExpr: "username"
                }
      }, {
            dataField: "user_to.name",
            caption: "TO: ",
            lookup: {
                    dataSource: DevExpress.data.AspNet.createStore({
                        key: "name",
                        loadUrl: "http://127.0.0.1:5000/users",
                        onBeforeSend: function(method, ajaxOptions) {
                            ajaxOptions.xhrFields = { withCredentials: true };
                        }
                    }),
                    displayExpr: "username"
                }
        }]
    }).dxDataGrid("instance");
});
