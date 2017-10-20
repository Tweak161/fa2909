-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.8.2
-- PostgreSQL version: 9.5
-- Project Site: pgmodeler.com.br
-- Model Author: ---

SET check_function_bodies = false;
-- ddl-end --

-- object: fa2909 | type: ROLE --
-- DROP ROLE IF EXISTS fa2909;
--CREATE ROLE fa2909 WITH 
--	SUPERUSER
--	INHERIT
--	LOGIN
--	ENCRYPTED PASSWORD '********';
-- ddl-end --


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: fa2909 | type: DATABASE --
-- -- DROP DATABASE IF EXISTS fa2909;
-- CREATE DATABASE fa2909
-- 	TABLESPACE = pg_default
-- ;
-- -- ddl-end --
-- 

-- object: "uuid-ossp" | type: EXTENSION --
-- DROP EXTENSION IF EXISTS "uuid-ossp" CASCADE;
--CREATE EXTENSION "uuid-ossp"
--      WITH SCHEMA public
--      VERSION '1.0';
-- ddl-end --
--COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';
-- ddl-end --

-- object: public.data | type: TABLE --
-- DROP TABLE IF EXISTS public.data CASCADE;

CREATE TABLE public.data(
	id uuid NOT NULL DEFAULT uuid_generate_v1(),
	time timestamp,
	part_id integer NOT NULL,
	component_id integer NOT NULL,
	processed bool NOT NULL DEFAULT false,
	classified bool NOT NULL DEFAULT false,
	data jsonb NOT NULL

);

-- ddl-end --


