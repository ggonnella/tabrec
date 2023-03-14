# InTabRec: a format for addressing records and fields in tabular record files

## Purpose

The ability to address a record of given type or single field or a set of
fields in tabular record files is useful for example for validations (e.g.
which fields may contain which value; which records may contain which tags) and
values extractions.

## Features

- address records of a given type
- address records of a given type and given subtypes,
  if subtypes are defined for a record type
- address multiple subtypes with a compact syntax
- address a single field or multiple fields with a compact syntax
- address fields of all records of a given type
- address fields of records of given type and subtypes
- address fields of multiple subtypes with a compact syntax

## Conventions

The record type is contained in the first field of each line. The subtype, if
exists, can be in any of the fields (default), but extraction methods allows to
specify a column number for the subtype.

The extraction methods allows specifying a subtype column, if a subtype exists.
If not specified, the subtype string is searched in all columns.

The positional fields can be addressed by their number (1-based)
or by name. In the latter case, a fields name string must be provided
(see below for the format specification).

## Specification

### Fields address string

A fields address string consists of one or a list of field address substrings,
separated by semicolons (;).

Each substring starts with a record type, optionally followed by a subtype or
a list of subtypes, and always followed by a field specifier or list of field
specifiers.

The record type is separated by a colon (:) from the optional subtype or list of
subtypes. If multiple subtypes are given, the list of subtypes is separated by
vertical lines (|).

The record type or subtypes are separated by a dot (.) from the field
specifiers. If multiple field specifiers are given, the list of field
specifiers is separated by vertical lines (|).

List specifiers are either field numbers of field names.
If field numbers are used, they are 1-based numbers larger than 1
(field 1 contains the record type and cannot be addressed).

Field names cannot contain only numerical characters. They are either
tag names or names of positional fields. In the latter case, applications
must be provided with a field names list (see below).

An example of fields address string is:
``G:taxon|strain.def;G.name``. The string would address fields
of type ``name`` from all records of type ``G`` and also the ``def``
fields if those records are of subtype ``taxon`` or ``strain``.

### Records address string

A record address string is similar to a fields address string but without
the fields part.
I.e. it is a list, separated by semicolons, of record address substrings.
Record address substrings always start with a record type, and may
(after a colon) specify one or multiple subtypes (separated by vertical lines).

An example of fields address string is:
``G:taxon|strain;C``. The string would address all records of type ``C``
and those records of type ``G`` with the subtype ``taxon`` or ``strain``.

### Field names list

A field names list must be provided to applications when the names of
positional fields are used in the fields address.

It consists of a list, separated by semicolon (;) of record types fieldnames
specifiers.
Each record type fieldnames specifier consists of the record type, a colon,
(:) and a list of field names, separated by ','. These are the names of the
positional fields after the record type, in the order.

For example
``G:id,name,type,def;D:id,link`` specifies that records of type ``G`` has the
fields ``record_type``, ``id``, ``name``, ``type``, ``def`` eventually
followed by tags, and records of type ``D`` have ``record_type``, ``id``
and ``link``, eventually followed by tags.

## Implementations

A parser and extraction tool based on the specification given above are
contained in the module ``tabrec_addressing``.

Furthermore, an implementation of the specifications given above as TextFormats
specification is contained in the package data file ``intabrec.tf.yaml``.

