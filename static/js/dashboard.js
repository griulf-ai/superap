$(document).ready(function () {
    $('#stocks-table').DataTable({
        pageLength: 50,
        order: [[5, 'asc']],  // Sort by Score (rec_mean) ascending = strongest buy first
        columnDefs: [
            { orderable: false, targets: [0] },  // Rank column not sortable
            { type: 'num', targets: [5, 6, 7, 8, 9, 10] }
        ],
        language: {
            search: 'Filter:',
            info: 'Showing _START_ to _END_ of _TOTAL_ stocks',
            lengthMenu: 'Show _MENU_ stocks',
        }
    });

    // Manual refresh button
    $('#refresh-btn').on('click', function () {
        var btn = $(this);
        btn.prop('disabled', true).text('Refreshing...');

        $.ajax({
            url: '/api/refresh',
            method: 'POST',
            success: function () {
                btn.text('Refresh started — reload page in ~30 min');
            },
            error: function () {
                btn.prop('disabled', false).text('Refresh Data');
                alert('Failed to start refresh. Please try again.');
            }
        });
    });
});
