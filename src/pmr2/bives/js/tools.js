var cache_key = 'bives_fileentry_cache';
var entry_table_body_path = '#bives_fileentry table tbody';

function check_localstorage() {
    return 'localStorage' in window && window['localStorage'] !== null;
}

function fetch_fileentry_cache() {
    try {
        return JSON.parse(localStorage[cache_key]);
    }
    catch (e) {
        return {};
    }
}

function clear_fileentries(entry) {
    if (!check_localstorage()) { return }
    localStorage[cache_key] = "{}";
    render_fileentry();
}

function add_fileentry(entry) {
    if (!check_localstorage()) { return }
    var fileentry = fetch_fileentry_cache();

    var rev = entry['rev'];
    var physical_path = entry['physical_path'];
    var file_path = entry['file_path'];

    if (!((typeof(rev) === 'string')
        && (typeof(physical_path) === 'string')
        && (typeof(file_path) === 'string')
            )) {
        return false;
    }

    fileentry[[physical_path, rev, file_path].join('/')] = entry;
    localStorage[cache_key] = JSON.stringify(fileentry);
    return true;
}

function render_fileentry() {
    if (!check_localstorage()) { return }
    var entries = fetch_fileentry_cache();
    var entry_table_body = $(entry_table_body_path);
    entry_table_body.html('');
    for (key in entries) {
        var entry = entries[key];
        var tr = $('<tr></tr>')
        tr.append($('<td></td>').text(entry['workspace_name']).append(
            $('<span style="color:#666"></span>').text(' @ ' +
                entry['rev'].substr(0, 12))
        ));
        tr.append($('<td></td>').text(entry['file_path']));
        tr.append($('<td></td>').append(
            $('<input type="radio" name="bives.source" />').attr(
                'value', key)));
        tr.append($('<td></td>').append(
            $('<input type="radio" name="bives.target" />').attr(
                'value', key)));
        entry_table_body.append(tr);
    }
}

$(entry_table_body_path).ready(render_fileentry);

$(document).ready(function() {
    $('#btn_bives_fileentry_pick').click(function() {
        entries = fetch_fileentry_cache();
        file1 = $('input[name="bives.source"]:checked').val();
        file2 = $('input[name="bives.target"]:checked').val();
        if (!file1 || !file2) {
            return false;
        }
        
        $('input[name="form.widgets.file1"]').val(
            JSON.stringify(entries[file1]));
        $('input[name="form.widgets.file2"]').val(
            JSON.stringify(entries[file2]));
        $('#bives_call').submit()
    });

    $('#btn_bives_fileentry_clear').click(clear_fileentries);
});

