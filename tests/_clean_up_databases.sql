/**
 Script to clean up the resources (databases + roles) created by Djereo's meta-project
 tests.

 Usage:
 ```
 psql \
   -U $(whoami) \
   -d postgres \
   -f _clean_up_databases.sql
 ```
**/

SELECT 'Running tests/_clean_up_databases.sql' AS msg;


\set pattern 'djereo_test_%'

-- terminate sessions
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname LIKE :'pattern'
  AND pid <> pg_backend_pid();

-- drop databases
SELECT 'DROP DATABASE IF EXISTS ' || quote_ident(datname) || ';'
FROM pg_database
WHERE datname LIKE :'pattern'
\gexec

-- drop roles
SELECT 'DROP ROLE IF EXISTS ' || quote_ident(rolname) || ';'
FROM pg_roles
WHERE rolname LIKE :'pattern'
\gexec
