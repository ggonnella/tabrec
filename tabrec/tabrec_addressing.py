# Methods for addressing single or multiple fields in tabular records

def extract_by_address(row, address, subtype_column = None):
  extracted = {}
  record_type_column = 0
  rt = row[record_type_column]
  if rt in address:
    for subtype in address[rt]:
      subtype_match = False
      if subtype is None:
        subtype_match = True
      elif subtype_column is None:
        subtype_match = subtype in row
      else:
        subtype_match = row[subtype_column] == subtype
      if subtype_match:
        for fn in address[rt][subtype]:
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
def parse_record_address(address_string):
  parts = address_string.split(';')
  address = {}
  for part in parts:
    if ':' in part:
      record_type, subtypes = part.split(':')
      subtypes = subtypes.split('|') if '|' in subtypes else [subtypes]
    else:
      record_type = part
      subtypes = [None]
    if record_type not in address:
      address[record_type] = []
    address[record_type].extend(subtypes)
  return address

# parses strings like 'RT:st|st.fn|fn;RT:st.fn|fn;RT.fn'
def parse_fields_address(address_string, fieldnames = None):
  parts = address_string.split(';')
  address = {}
  for part in parts:
    if '.' not in part:
      e = "Error: fields address part does not contain field names\n" +\
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
    if record_type not in address:
      address[record_type] = {}
    if not subtypes:
      if None not in address[record_type]:
        address[record_type][None] = []
      address[record_type][None].extend(fields)
    else:
      for subtype in subtypes:
        if subtype not in address[record_type]:
          address[record_type][subtype] = []
        address[record_type][subtype].extend(fields)
  return address

