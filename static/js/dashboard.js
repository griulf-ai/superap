$(document).ready(function () {
    var table = $('#stocks-table').DataTable({
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

    var pollInterval = null;
    var tableRefreshInterval = null;

    function formatMarketCap(val) {
        if (!val) return 'N/A';
        if (val >= 1e12) return '$' + (val / 1e12).toFixed(1) + 'T';
        if (val >= 1e9) return '$' + (val / 1e9).toFixed(1) + 'B';
        if (val >= 1e6) return '$' + Math.round(val / 1e6) + 'M';
        return '$' + Math.round(val);
    }

    function formatUpside(val) {
        if (val === null || val === undefined) return 'N/A';
        var cls = val > 0 ? 'text-green' : val < 0 ? 'text-red' : '';
        var sign = val > 0 ? '+' : '';
        return '<span class="' + cls + '">' + sign + val.toFixed(1) + '%</span>';
    }

    function badgeClass(recKey) {
        return 'badge badge-' + (recKey || 'none');
    }

    function badgeLabel(recKey) {
        if (!recKey) return 'N/A';
        return recKey.replace(/_/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
    }

    function refreshTable() {
        $.getJSON('/api/stocks', function (data) {
            // Update meta info
            var countText = data.stock_count + ' stocks';
            var updateText = data.last_update
                ? ' \u00b7 Last updated: ' + data.last_update.substring(0, 19) + ' UTC'
                : '';
            $('.meta').html(countText + updateText);

            // Rebuild table
            table.clear();
            for (var i = 0; i < data.stocks.length; i++) {
                var s = data.stocks[i];
                table.row.add([
                    i + 1,
                    '<a href="/stock/' + s.ticker + '">' + s.ticker + '</a>',
                    s.company_name || 'N/A',
                    s.sector || 'N/A',
                    '<span class="' + badgeClass(s.rec_key) + '">' + badgeLabel(s.rec_key) + '</span>',
                    s.rec_mean !== null ? s.rec_mean.toFixed(2) : 'N/A',
                    s.num_analysts || 'N/A',
                    s.current_price !== null ? '$' + s.current_price.toFixed(2) : 'N/A',
                    s.target_mean !== null ? '$' + s.target_mean.toFixed(2) : 'N/A',
                    formatUpside(s.upside_pct),
                    formatMarketCap(s.market_cap),
                ]);
            }
            table.draw(false);

            // If the table was empty and now has data, remove empty state
            if (data.stocks.length > 0) {
                $('.empty-state').remove();
                if ($('#stocks-table').closest('.dataTables_wrapper').length === 0) {
                    // Table needs to be re-initialized — reload page once
                    location.reload();
                }
            }
        });
    }

    function pollRefreshStatus() {
        $.getJSON('/api/refresh/status', function (status) {
            if (status.in_progress) {
                showProgress(status);
            } else if (pollInterval) {
                // Refresh just finished
                hideProgress();
                stopPolling();
                refreshTable();
                $('#refresh-btn').prop('disabled', false).text('Refresh Data');
            }
        });
    }

    function showProgress(status) {
        var $container = $('#refresh-progress');
        $container.show();

        var pct = status.total > 0 ? Math.round((status.processed / status.total) * 100) : 0;
        $('#progress-bar-fill').css('width', pct + '%');
        $('#progress-count').text(status.processed + ' / ' + status.total);
        $('#progress-text').text(
            'Fetching stock data... (' + status.success + ' OK, ' + status.failed + ' failed)'
        );
    }

    function hideProgress() {
        $('#refresh-progress').hide();
    }

    function startPolling() {
        // Poll status every 5 seconds
        pollInterval = setInterval(pollRefreshStatus, 5000);
        // Refresh table every 15 seconds
        tableRefreshInterval = setInterval(refreshTable, 15000);
    }

    function stopPolling() {
        if (pollInterval) {
            clearInterval(pollInterval);
            pollInterval = null;
        }
        if (tableRefreshInterval) {
            clearInterval(tableRefreshInterval);
            tableRefreshInterval = null;
        }
    }

    // Manual refresh button
    $('#refresh-btn').on('click', function () {
        var btn = $(this);
        btn.prop('disabled', true).text('Refreshing...');

        $.ajax({
            url: '/api/refresh',
            method: 'POST',
            success: function () {
                startPolling();
                // Initial poll immediately
                pollRefreshStatus();
            },
            error: function () {
                btn.prop('disabled', false).text('Refresh Data');
                alert('Failed to start refresh. Please try again.');
            }
        });
    });

    // Check on page load if a refresh is already running
    $.getJSON('/api/refresh/status', function (status) {
        if (status.in_progress) {
            $('#refresh-btn').prop('disabled', true).text('Refreshing...');
            showProgress(status);
            startPolling();
        }
    });
});
