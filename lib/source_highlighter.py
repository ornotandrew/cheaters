
def highlight(file, match_ranges, index):
    """
    :param file: source code to highlight
    :param match_ranges: list of lines to highlight
    :param index: 0 or 1, which file it is in the match_ranges list
    :return: source with added html to highlight lines
    """
    col = ["#cc3f3f ", "#379fd8", "#87c540", "#be7cd2", "#ff8ecf", "#e5e155"]

    source = file.splitlines()
    for i, match_range in enumerate(match_ranges):
        for match in match_range:
            line = match[index]
            source[line-1] = r'<span style="color:'+col[i % len(col)]+r';">'+source[line-1]+r'</span>'

    return "\n".join(source)