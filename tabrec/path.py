# Selecting and extracting single or multiple fields or records
# from tabular records file

def extract_fields(row, fields_path, subtype_column = None):
  """
  Extracts fields from a row of a tabular records file.

  Parameters
  ----------
  row : list of str (the fields of a record)
  fields_path : the parsed fields path (see parse_fields_path)
  subtype_column : int, optional (default: None)
                   if provided (as a 0-based column number)
                   the subtype string is searched in that column;
                   otherwise the subtype strings are searched
                   in all columns

  Returns
  -------
  dict : if the record type and subtype match the path,
         the fields are extracted and returned as dict values
         (the keys are the field names or numbers);
         if there is no match, an empty dict is returned
  """
  extracted = {}
  record_type_column = 0
  rt = row[record_type_column]
  if rt in fields_path:
    for subtype in fields_path[rt]:
      subtype_match = False
      if subtype is None:
        subtype_match = True
      elif subtype_column is None:
        subtype_match = subtype in row
      else:
        subtype_match = row[subtype_column] == subtype
      if subtype_match:
        for fn in fields_path[rt][subtype]:
          # if field is a number, it is a column number, else a tag name
          if isinstance(fn, int):
            extracted[fn] = row[fn]
          else:
            for cell in row:
              tag_parts = cell.split(':', 2)
              if len(tag_parts) == 3 and tag_parts[0] == fn:
                extracted[fn] = cell[2]
  return extracted

# parses strings like 'RT:st|st;RT;RT:st;...'
def parse_records_path(records_path):
  """
  Parses a records path string.

  The result is a dict, with a key for each record type, and a list of
  subtypes or None (for selecting the record type independently of subtypes)
  as value.

  Examples
  --------

  >>> parse_records_path('RT1;RT2:st3;RT4:st5|st6')

  {'RT1': [None], 'RT2': ['st3'], 'RT4': ['st5', 'st6']}

  Parameters
  ----------
  records_path : str

  Returns
  -------
  dict : the parsed fields path (dict of dicts of lists)
           dict: record type
             dict: subtype or None (for no subtype)
               list: field selectors (positional field numbers or tag names)
  """
  parts = records_path.split(';')
  result = {}
  for part in parts:
    if ':' in part:
      record_type, subtypes = part.split(':')
      subtypes = subtypes.split('|') if '|' in subtypes else [subtypes]
    else:
      record_type = part
      subtypes = [None]
    if record_type not in result:
      result[record_type] = []
    result[record_type].extend(subtypes)
  return result


# parses strings like 'RT:st|st.fn|fn;RT:st.fn|fn;RT.fn'
def parse_fields_path(fields_path, fieldnames = None):
  """
  Parses a fields path string.

  If the field path string contains field names, the fieldnames parameter must
  be provided (a list of field names for each of the record types in the path).

  The result gives lists of the selected fields for each record type
  and subtype. The results are returned as a dict of dicts of lists.
  The first dict has record types as keys, the second dict has
  subtypes or None (for fields selected independently of the subtype) as keys,
  and the lists contain the selected positional field numbers (0-based)
  and tag names.

  Examples
  --------

  >>> parse_fields_path('RT1.2|4;RT4:st5.XY;RT7:st8|st9.3|XX')

  {'RT1': {None: [2, 4]},
   'RT4': {'st5': ['XY']},
   'RT7': {'st8': [3, 'XX'], 'st9': [3, 'XX']}}

  >>> parse_fields_path('RT1.aaa|ccc;RT4:st5.XY;RT7:st8|st9.baz|XX',\
                        {'RT1': ['aaa', 'bbb', 'ccc', 'ddd'],\
                         'RT7': ['foo', 'bar', 'baz', 'qux']})

  {'RT1': {None: [2, 4]},
   'RT4': {'st5': ['XY']},
   'RT7': {'st8': [3, 'XX'], 'st9': [3, 'XX']}}

  Parameters
  ----------
  fields_path : str
  fieldnames : dict (default: None, i.e. interpret field selectors as numbers or
               tag names) for each record type (key) a list of names of the
               fields after the record type field (value);

  Returns
  -------
  dict : the parsed fields path (dict of dicts of lists)
           dict: record type
             dict: subtype or None (for no subtype)
               list: field selectors (positional field numbers or tag names)
  """
  parts = fields_path.split(';')
  result = {}
  for part in parts:
    if '.' not in part:
      e = "Error: fields result part does not contain field names\n" +\
          f"Found: {part}\n"
      raise ValueError(e)
    rtst_part, fields_part = part.split('.')
    fields = fields_part.split('|') if '|' in fields_part else [fields_part]
    if ':' in rtst_part:
      record_type, st_part = rtst_part.split(':')
      subtypes = st_part.split('|') if '|' in st_part else [st_part]
    else:
      record_type = rtst_part
      subtypes = []
    fields = [int(fn) if fn.isdigit() else fn for fn in fields]
    if fieldnames and record_type in fieldnames:
      rtfn = fieldnames[record_type]
      fields = [rtfn.index(fn) + 1 if fn in rtfn else fn for fn in fields]
    if record_type not in result:
      result[record_type] = {}
    if not subtypes:
      if None not in result[record_type]:
        result[record_type][None] = []
      result[record_type][None].extend(fields)
    else:
      for subtype in subtypes:
        if subtype not in result[record_type]:
          result[record_type][subtype] = []
        result[record_type][subtype].extend(fields)
  return result

def parse_fieldnames(arg):
  if not arg:
    return None
  fieldnames = {}
  for spec in arg.split(";"):
    if ':' not in spec:
      errmsg = "Error: fieldnames must be in the form "+\
          "'record_type:name,name,name;record_type:name,name,name'\n"+\
          f"Found: {spec}\n"
      raise ValueError(errmsg)
    rt, names = spec.split(':')
    names = names.split(',')
    fieldnames[rt] = names
  return fieldnames

