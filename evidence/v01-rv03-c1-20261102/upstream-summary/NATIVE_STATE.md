# Native verification state retention

The 77 native acceptance schedules retain their original disposable SQLite, WAL and shared-memory snapshots locally under acceptance-schedules/. The 231 database files follow ARH’s existing Git ignore convention and are not part of the code commit. Their exact local bytes and hashes are listed in native-state-manifest.json. Do not mistake a clone without these local fixtures for a retained database. No database bytes were rewritten for packaging.

The versioned evidence-manifest.json covers public traces, commands, outcomes, source archives, regression records and this separate native-state manifest. Murmur consumes public exports only and never reads these native databases. Authentication connection/config files and actor tokens are excluded.
