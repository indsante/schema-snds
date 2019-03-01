#!/usr/bin/env bash
echo 'Running schema crawler against PostgreSQL'

/opt/schemacrawler/schemacrawler.sh -command=brief \
-infolevel=standard \
-portablenames=true \
-server=postgresql -host=postgres -port=5432 -user=postgres -database=postgres \
-title 'Schema DCIR et DCIRS' \
-only-matching \
-outputformat=pdf -outputfile=/share/schema_postgres.pdf

echo 'Done. Relational diagram has been written in data/diagram'
