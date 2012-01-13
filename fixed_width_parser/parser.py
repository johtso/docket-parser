from utils import pairwise, iterchunks

def parse_line(line, fields):
    """Parses a line of fixed width data.
    Fields should be a list of tuples of form:
    (field_start, field_name), field_start being the column number at which the
    field begins.

    """
    data = {}
    field_starts = [field[0] for field in fields]
    # Construct slices ranging from the start of each field to the start of the
    # next field.
    slices = [slice(a, b) for a, b in pairwise(field_starts + [None])]
    for slice_, field in zip(slices, fields):
        field_name = field[1]
        value = line[slice_].strip()
        data[field_name] = value
    return data

def parse_entry(lines, fields):
    """Takes a sequence of fixed width data lines, and extracts the data, mapping
    it to the field names, and returning a dictionary.

    """
    parsed_entry = {}
    for line, line_fields in zip(lines, fields):
        line_data = parse_line(line, line_fields)
        parsed_entry = dict(parsed_entry, **line_data)
    return parsed_entry

def iterparse_lines(lines, fields):
    rows_per_entry = len(fields)
    for line_group in iterchunks(lines, rows_per_entry):
        parsed_entry = parse_entry(line_group, fields)
        yield parsed_entry