var VERSION = 1;
var version_key = 'bives_fileentry_version';
var cache_key = 'bives_fileentry_cache';
var entry_table_body_path = '#bives_fileentry table tbody';
var has_localStorage = ('localStorage' in window &&
    window['localStorage'] !== null);


function format_localStorage() {
    localStorage[cache_key] = "{}";
    localStorage[version_key] = VERSION;
}

function fetch_fileentry_cache() {
    if (!has_localStorage) {
        return {}
    }

    try {
        if (!(localStorage[version_key] >= VERSION)) {
            throw "Version out of date";
        }
        return JSON.parse(localStorage[cache_key]);
    }
    catch (e) {
        // Data in localStorage is corrupted so just clear that.
        format_localStorage();
        return {};
    }
}

function clear_fileentries(entry) {
    if (!has_localStorage) { return }
    format_localStorage();
    render_fileentry();
}

function add_fileentry(entry) {
    if (!has_localStorage) { return }
    var fileentry = fetch_fileentry_cache();

    var rev = entry['rev'];
    var physical_path = entry['physical_path'];
    var file_path = entry['file_path'];
    var href = entry['href'];

    if (!((typeof(rev) === 'string')
        && (typeof(physical_path) === 'string')
        && (typeof(file_path) === 'string')
        && (typeof(href) === 'string')
            )) {
        return false;
    }

    fileentry[[physical_path, rev, file_path].join('/')] = entry;
    localStorage[cache_key] = JSON.stringify(fileentry);
    return true;
}

function render_fileentry() {
    var entries = fetch_fileentry_cache();
    var entry_table_body = $(entry_table_body_path);
    entry_table_body.html('');
    for (key in entries) {
        var entry = entries[key];
        var tr = $('<tr></tr>')
        var td = $('<td></td>')

        if (entry['portal_type'] == 'Workspace') {
            td.append($('<a></a>').attr('href', entry['href']).text(''
            + entry['obj_name']
            + ' @ '
            + entry['rev'].substr(0, 12)
            + ' / '
            + entry['file_path']
            ));
        }
        else if (entry['portal_type'] == 'ExposureFile') {
            td.append($('<a></a>').attr('href', entry['href']).text(
                entry['obj_name']));
        }
        else {
            td.append($('<a></a>').attr('href', entry['href']).text('Unknown'));
        }

        tr.append(td);
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
        file1 = $('input[name="bives.source"]:checked').val();
        file2 = $('input[name="bives.target"]:checked').val();
        if (!file1 || !file2) {
            return false;
        }
        
        entries = fetch_fileentry_cache();
        $('input[name="form.widgets.file1"]').val(
            JSON.stringify(entries[file1]));
        $('input[name="form.widgets.file2"]').val(
            JSON.stringify(entries[file2]));
        $('#bives_call').submit()
    });

    $('#btn_bives_fileentry_clear').click(clear_fileentries);
});
