-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.8.2
-- PostgreSQL version: 9.5
-- Project Site: pgmodeler.com.br
-- Model Author: ---

SET check_function_bodies = false;
-- ddl-end --

-- object: gtlog | type: ROLE --
-- DROP ROLE IF EXISTS gtlog;
CREATE ROLE gtlog WITH 
	SUPERUSER
	INHERIT
	LOGIN
	ENCRYPTED PASSWORD '********';
-- ddl-end --


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: gtlog | type: DATABASE --
-- -- DROP DATABASE IF EXISTS gtlog;
-- CREATE DATABASE gtlog
-- 	TABLESPACE = pg_default
-- ;
-- -- ddl-end --
-- 

-- object: "uuid-ossp" | type: EXTENSION --
-- DROP EXTENSION IF EXISTS "uuid-ossp" CASCADE;
CREATE EXTENSION "uuid-ossp"
      WITH SCHEMA public
      VERSION '1.0';
-- ddl-end --
COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';
-- ddl-end --

-- object: public.component | type: TABLE --
-- DROP TABLE IF EXISTS public.component CASCADE;
CREATE TABLE public.component(
	id integer NOT NULL,
	name character varying(100) NOT NULL,
	description text,
	CONSTRAINT component_name_key UNIQUE (name),
	CONSTRAINT component_pkey PRIMARY KEY (id)

);
-- ddl-end --

-- object: public.data | type: TABLE --
-- DROP TABLE IF EXISTS public.data CASCADE;
CREATE TABLE public.data(
	id uuid NOT NULL DEFAULT uuid_generate_v1(),
	run uuid NOT NULL,
	tmono timestamp,
	tlocal timestamp,
	tutc timestamp,
	msgtype integer NOT NULL,
	seqnr integer NOT NULL,
	data jsonb NOT NULL,
	CONSTRAINT "data_un_RunMsgtypeSeqnr" UNIQUE (run,msgtype,seqnr)

);
-- ddl-end --

-- object: public.msgtype | type: TABLE --
-- DROP TABLE IF EXISTS public.msgtype CASCADE;
CREATE TABLE public.msgtype(
	id integer NOT NULL,
	shortname character varying(100) NOT NULL,
	name text,
	description text,
	CONSTRAINT type_pkey PRIMARY KEY (id),
	CONSTRAINT type_shortname_key UNIQUE (shortname)

);
-- ddl-end --

-- object: public.run | type: TABLE --
-- DROP TABLE IF EXISTS public.run CASCADE;
CREATE TABLE public.run(
	id uuid NOT NULL DEFAULT uuid_generate_v1(),
	tlocal timestamp DEFAULT now(),
	tutc timestamp,
	comment text,
	location text,
	vehicle integer NOT NULL,
	active bool NOT NULL DEFAULT false,
	seqnr integer NOT NULL DEFAULT 0,
	CONSTRAINT run_pkey PRIMARY KEY (id)

);
-- ddl-end --

-- object: "data_in_RunMsgtypeSeqnr" | type: INDEX --
-- DROP INDEX IF EXISTS public."data_in_RunMsgtypeSeqnr" CASCADE;
CREATE INDEX "data_in_RunMsgtypeSeqnr" ON public.data
	USING btree
	(
	  id,
	  msgtype ASC NULLS LAST,
	  seqnr ASC NULLS LAST
	);
-- ddl-end --

-- object: public.data_insert | type: FUNCTION --
-- DROP FUNCTION IF EXISTS public.data_insert(IN integer,IN timestamp,IN timestamp,IN integer,IN jsonb) CASCADE;
CREATE FUNCTION public.data_insert (IN vehicle integer, IN tmono timestamp, IN tlocal timestamp, IN msgtype integer, IN data jsonb)
	RETURNS bool
	LANGUAGE plpgsql
	VOLATILE 
	COST 1
	AS $$
DECLARE
  run_tmp uuid;
  seqnr_tmp integer;
BEGIN
  -- find current run id
  SELECT run.id INTO run_tmp FROM run
   WHERE run.vehicle = data_insert.vehicle AND run.active = true
   LIMIT 1;

  -- find current seqence number of this message type for this vehicle
  SELECT vehicle_component_msgtype.seqnr INTO seqnr_tmp FROM vehicle_component_msgtype
   WHERE vehicle_component_msgtype.msgtype = data_insert.msgtype AND vehicle_component_msgtype.vehicle = data_insert.vehicle
   LIMIT 1;

  -- no seqence number found = this combination of vehicle / message is not defined -> error
  IF seqnr_tmp IS NULL THEN
    RETURN false;
  END IF;

  seqnr_tmp = seqnr_tmp +1;

  -- updates data for telemetry and sequence number
  UPDATE vehicle_component_msgtype SET seqnr = seqnr_tmp, lasttlocal = data_insert.tlocal, lastdata = data_insert.data WHERE vehicle_component_msgtype.msgtype = data_insert.msgtype AND vehicle_component_msgtype.vehicle = data_insert.vehicle;

  -- no active run -> telemetry only, no logging
  IF run_tmp IS NULL THEN
    RETURN false;
  END IF;

  -- log data
  INSERT INTO data
   (run, tmono, tlocal, tutc, msgtype, seqnr, data)
  VALUES
   (run_tmp, data_insert.tmono, data_insert.tlocal, NULL, data_insert.msgtype, seqnr_tmp, data_insert.data);

  RETURN true;

EXCEPTION
  WHEN OTHERS OR QUERY_CANCELED THEN
    RETURN false;

END;

$$;
-- ddl-end --

-- object: public.vehicle | type: TABLE --
-- DROP TABLE IF EXISTS public.vehicle CASCADE;
CREATE TABLE public.vehicle(
	id integer NOT NULL,
	name character varying(100) NOT NULL,
	description text,
	CONSTRAINT vehicle_name_key UNIQUE (name),
	CONSTRAINT vehicle_pkey PRIMARY KEY (id)

);
-- ddl-end --

-- object: public.vehicle_component_msgtype | type: TABLE --
-- DROP TABLE IF EXISTS public.vehicle_component_msgtype CASCADE;
CREATE TABLE public.vehicle_component_msgtype(
	id integer NOT NULL,
	vehicle integer NOT NULL,
	component integer NOT NULL,
	msgtype integer NOT NULL,
	seqnr integer NOT NULL DEFAULT 0,
	lastdata jsonb,
	lasttlocal timestamp,
	CONSTRAINT vehicle_component_msgtype_pkey PRIMARY KEY (id),
	CONSTRAINT vehicle_msgtype_un UNIQUE (vehicle,msgtype)

);
-- ddl-end --

CREATE FUNCTION public.run_stop (IN vehicle integer)
	RETURNS void
	LANGUAGE plpgsql
	VOLATILE
	COST 1
	AS $$
	BEGIN
		UPDATE run SET active = false WHERE run.vehicle = run_stop.vehicle;
	END;
$$;

-- object: public.run_new | type: FUNCTION --
-- DROP FUNCTION IF EXISTS public.run_new(IN integer,IN timestamp,IN timestamp,IN text,IN text) CASCADE;
CREATE FUNCTION public.run_new (IN vehicle integer, IN tlocal timestamp, IN tutc timestamp, IN comment text, IN location text)
	RETURNS bool
	LANGUAGE plpgsql
	VOLATILE 
	COST 1
	AS $$
DECLARE
  seqnr_tmp integer;
BEGIN
  -- set old run of this vehicle inactive
  UPDATE run SET active = false WHERE run.vehicle = run_new.vehicle;

  -- find sequence number 
  SELECT MAX(run.seqnr) INTO seqnr_tmp FROM run WHERE run.vehicle = run_new.vehicle;
  IF seqnr_tmp IS NULL THEN
    seqnr_tmp = 0;
  ELSE
    seqnr_tmp = seqnr_tmp +1;
  END IF;

  -- create a new run
  INSERT INTO run
   (tlocal, tutc, comment, location, vehicle, active, seqnr)
  VALUES
   (run_new.tlocal, run_new.tutc,
    run_new.comment, run_new.location,
    run_new.vehicle, true,
    seqnr_tmp);

  -- clear telemetry data
  UPDATE vehicle_component_msgtype SET seqnr = 0, lastdata = NULL, lasttlocal = NULL WHERE vehicle_component_msgtype.vehicle = run_new.vehicle;
  RETURN true;

EXCEPTION
  WHEN OTHERS OR QUERY_CANCELED THEN
    RETURN false;

END;

$$;
-- ddl-end --
ALTER FUNCTION public.run_new(IN integer,IN timestamp,IN timestamp,IN text,IN text) OWNER TO postgres;
-- ddl-end --

-- object: public.telemetry_live | type: VIEW --
-- DROP VIEW IF EXISTS public.telemetry_live CASCADE;
CREATE VIEW public.telemetry_live
AS 

SELECT vehicle.id AS vehicle_id,
    vehicle.name AS vehicle_name,
    component.id AS component_id,
    component.name AS component_name,
    msgtype.id AS msgtype_id,
    msgtype.shortname AS msgtype_shortname,
    vehicle_component_msgtype.lastdata AS data,
    vehicle_component_msgtype.seqnr,
    vehicle_component_msgtype.lasttlocal AS tlocal
   FROM (((vehicle_component_msgtype
     JOIN vehicle ON ((vehicle_component_msgtype.vehicle = vehicle.id)))
     JOIN msgtype ON ((vehicle_component_msgtype.msgtype = msgtype.id)))
     JOIN component ON ((vehicle_component_msgtype.component = component.id)));
-- ddl-end --
ALTER VIEW public.telemetry_live OWNER TO gtlog;
-- ddl-end --

-- object: public.msgtype_info | type: VIEW --
-- DROP VIEW IF EXISTS public.msgtype_info CASCADE;
CREATE VIEW public.msgtype_info
AS 

SELECT vehicle.id AS vehicle_id,
    vehicle.name AS vehicle_name,
    component.id AS component_id,
    component.name AS component_name,
    msgtype.id AS msgtype_id,
    msgtype.shortname AS msgtype_shortname
   FROM (((vehicle_component_msgtype
     JOIN vehicle ON ((vehicle_component_msgtype.vehicle = vehicle.id)))
     JOIN component ON ((vehicle_component_msgtype.component = component.id)))
     JOIN msgtype ON ((vehicle_component_msgtype.msgtype = msgtype.id)));
-- ddl-end --
ALTER VIEW public.msgtype_info OWNER TO gtlog;
-- ddl-end --

CREATE VIEW public.logging_data
AS

SELECT 
   vehicle.id AS vehicle_id, 
   vehicle.name AS vehicle_name, 
   component.id AS component_id,
   component.name AS component_name, 
   msgtype.id AS msgtype_id,
   msgtype.shortname AS msgtype_shortname,
   run.id AS run_id,
   run.location AS run_location,
   run.seqnr AS run_seqnr,
   run.comment AS run_comment,
   data.tmono AS tmono,
   data.tlocal AS tlocal,
   data.tutc AS tutc,
   data.seqnr AS data_seqnr,
   data.data AS data
 FROM data 
 JOIN run ON data.run = run.id 
 JOIN vehicle ON run.vehicle = vehicle.id 
 JOIN msgtype ON data.msgtype = msgtype.id 
 JOIN vehicle_component_msgtype ON (data.msgtype = vehicle_component_msgtype.msgtype AND vehicle.id = vehicle_component_msgtype.vehicle) 
 JOIN component ON vehicle_component_msgtype.component = component.id;


CREATE VIEW public.run_list
AS

SELECT 
   run.id AS run_id,
   vehicle.id AS vehicle_id,
   vehicle.name AS vehicle_name,
   run.location AS location,
   run.comment AS comment,
   run.tlocal AS tlocal,
   run.tutc AS tutc,
   run.active AS active,
   run.seqnr AS seqnr
  FROM run
  JOIN vehicle ON run.vehicle = vehicle.id;


-- object: data_fk_run | type: CONSTRAINT --
-- ALTER TABLE public.data DROP CONSTRAINT IF EXISTS data_fk_run CASCADE;
ALTER TABLE public.data ADD CONSTRAINT data_fk_run FOREIGN KEY (run)
REFERENCES public.run (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: data_fk_msgtype | type: CONSTRAINT --
-- ALTER TABLE public.data DROP CONSTRAINT IF EXISTS data_fk_msgtype CASCADE;
ALTER TABLE public.data ADD CONSTRAINT data_fk_msgtype FOREIGN KEY (msgtype)
REFERENCES public.msgtype (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: run_fkey_vehicle | type: CONSTRAINT --
-- ALTER TABLE public.run DROP CONSTRAINT IF EXISTS run_fkey_vehicle CASCADE;
ALTER TABLE public.run ADD CONSTRAINT run_fkey_vehicle FOREIGN KEY (vehicle)
REFERENCES public.vehicle (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: vehicle_component | type: CONSTRAINT --
-- ALTER TABLE public.vehicle_component_msgtype DROP CONSTRAINT IF EXISTS vehicle_component CASCADE;
ALTER TABLE public.vehicle_component_msgtype ADD CONSTRAINT vehicle_component FOREIGN KEY (component)
REFERENCES public.component (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: vehicle_msgtype | type: CONSTRAINT --
-- ALTER TABLE public.vehicle_component_msgtype DROP CONSTRAINT IF EXISTS vehicle_msgtype CASCADE;
ALTER TABLE public.vehicle_component_msgtype ADD CONSTRAINT vehicle_msgtype FOREIGN KEY (msgtype)
REFERENCES public.msgtype (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: vehicle_vehicle | type: CONSTRAINT --
-- ALTER TABLE public.vehicle_component_msgtype DROP CONSTRAINT IF EXISTS vehicle_vehicle CASCADE;
ALTER TABLE public.vehicle_component_msgtype ADD CONSTRAINT vehicle_vehicle FOREIGN KEY (vehicle)
REFERENCES public.vehicle (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION;
-- ddl-end --

-- object: grant_774bcaa53a | type: PERMISSION --
GRANT CONNECT,TEMPORARY
   ON DATABASE gtlog
   TO PUBLIC;
-- ddl-end --


