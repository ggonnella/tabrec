# TabRecPath: selecting and extracting records and fields in tabular record files

## Purpose

The ability to select a record of given type or single field or a set of
fields in tabular record files is useful for example for validations (e.g.
which fields may contain which value; which records may contain which tags) and
values extractions.

## Features

The system offers various features for selecting records and fields based on
the record type and subtype (if subtypes exists for a record type).

Record paths allow selecting all records of a given type,
or records of a given type and subtype.
Multiple subtypes can be selected with a compact syntax.

Field paths allow selecting a single field or multiple fields (with a compact
syntax) in all records of a given type and optionally of a given subtype.

## Conventions

The record type must be in the first field of each record.

Subtypes can be in any field. Extraction methods shall allow to specify the
subtype column number and search the subtype string anywhere in the
record by default.

Record types, subtypes and field names shall not contain the following
characters: newline, tab, semicolon, colon, dot, vertical bar.

Field names may not consist of only digits.

## Specification

### Field selectors

Positional fields are selected by their column number, where 1 is the
field after the record type. In alternative, positional field names can be
used, and converted to numbers by providing a fields name string to the
parsing methods (see below for the format of this string).

Tags are selected by their name.

### Records path

A records path is a semicolon-separated list of records path elements.

Records path elements select a single record type, with or without subtypes
specifications. An element start with the record type,
and may (after a colon) specify one or multiple subtypes
(separated by vertical lines).

An example of records path string is: ``A;B:taxon|strain``. The
string selects records of type ``A`` and records of type ``B`` with the subtype
``taxon`` or ``strain``.

### Fields path

A fields path is a semicolon-separated list of fields path elements.

Each field path element selects one or multiple fields in records of one type.
It starts with a record type.

Subtypes may be optionally specified: if so,
a colon follows the record type, then the subtypes are given,
separated by vertical bars.

Finally, one or multiple field selectors are always given,
introduced by a dot, and separated by vertical bars.

An example of fields path string is: ``G:taxon|strain.def;G.2``. It selects the
second field after the record type, for of all records of type ``G`` and,
additionally, the ``def`` field, when the records of the same type are of
subtype ``taxon`` or ``strain``.

### Field names list

If positional field names are used as field selectors, instead of column
numbers, the parsing methods must be provided with lists of field names.
Such information can be passed as a string, consisting of field names
lists for each record type, separated by semicolons.

Each record type field names list consists of the record type, a colon,
(:) and the ordered list of names of the positional fields after the record
type field, separated by commas.

For example
``G:id,name,type,def;D:id,link`` specifies that records of type ``G`` has the
fields ``record_type`` (implicit), ``id``, ``name``, ``type``, ``def``
eventually followed by tags, and records of type ``D`` have ``record_type``
(implicit), ``id`` and ``link``, eventually followed by tags.

## Implementations

A parser and extraction tool based on the specification given above are
contained in the module ``tabrec.path``.

Furthermore, an implementation of the specifications given above as TextFormats
specification is contained in the package data file ``tabrecpath.tf.yaml``.

## Additional idea, not implemented in the current version

The format can be extended to allow for field value queries.

Field value queries are lists of key value pairs, separated by ampersand
(``&``). The key and values are separated by an equal sign (``=``) . The keys
are field selector and the value are (possibly empty) strings, not enclosed in
quotes.

The list of forbidden characters in identifiers must be extended to
include the equal sign and ampersand. The string values of the fields
shall also be disallowed to include the forbidden characters.

Both fields paths and records paths can support field value queries. Field
values queries and subtypes can be mixed. An example of record path string with
fields queries is: ``X:1=&XR=1|foo|2=a``. The string selects records of type
``X`` with either the subtype ``foo`` or an empty string in the first field and
the value "1" in the XR field, or the value "a" in the second field.

## Acknowledgements

This specification has been created in context of the DFG project GO 3192/1-1
“Automated characterization of microbial genomes and metagenomes by collection
and verification of association rules”. The funders had no role in study
design, data collection and analysis.

