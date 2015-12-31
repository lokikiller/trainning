/**
 * Created by hty on 15/11/19.
 */

getHostList();

function getHostList() {
    $('#tablebody').html('');

    $.ajax({
        type: 'get',
        url: '/host/list',
        dataType: 'json',
        success: function (array) {
            tableStr = "";
            for (var i = 0; i < array.length; i++) {
                var obj = array[i];
                var cpu = new Number(obj.hostCPU * 100);
                var memory = new Number(obj.hostMemory * 100);
                var thiStr = '<tr rowid=' + obj.hostIP + '><td>' + obj.hostIP +
                    '</td><td>' + obj.hostLoad + '</td><td>' + cpu.toFixed(3) +
                    '%</td><td>' + memory.toFixed(3) + '%</td>' +
                    '<td><a class="id">详情</a></td></tr>';
                tableStr += thiStr;
            }
            $('#tablebody').html(tableStr);
        }
    });
}

$('#tablebody').on('click', '.id', function (event) {
    event.preventDefault();
    var uuid = $(this).parents('tr').attr('rowid');
    var form = $("<form></form>");
    form.attr("action", "/host/detail");
    form.attr("method", "post");
    var input = $('<input type="text" name="hostUuid" value="'+ uuid +'" />');
    form.append(input);
    form.css('display', 'none');
    form.appendTo($('body'));
    form.submit();
});