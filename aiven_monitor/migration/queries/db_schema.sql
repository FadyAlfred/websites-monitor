--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6
-- Dumped by pg_dump version 15.1

-- Started on 2023-01-14 12:50:51 CET

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 212 (class 1259 OID 16425)
-- Name: monitor_records; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.monitor_records (
    id bigint NOT NULL,
    site_id bigint NOT NULL,
    response_time numeric NOT NULL,
    status_code text NOT NULL,
    is_content_matched text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.monitor_records OWNER TO avnadmin;

--
-- TOC entry 211 (class 1259 OID 16424)
-- Name: monitor_records_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

ALTER TABLE public.monitor_records ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.monitor_records_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 210 (class 1259 OID 16416)
-- Name: websites; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.websites (
    id integer NOT NULL,
    url text NOT NULL,
    regex text,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.websites OWNER TO avnadmin;

--
-- TOC entry 209 (class 1259 OID 16415)
-- Name: websites_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.websites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.websites_id_seq OWNER TO avnadmin;

--
-- TOC entry 4331 (class 0 OID 0)
-- Dependencies: 209
-- Name: websites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.websites_id_seq OWNED BY public.websites.id;


--
-- TOC entry 4177 (class 2604 OID 16419)
-- Name: websites id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.websites ALTER COLUMN id SET DEFAULT nextval('public.websites_id_seq'::regclass);


--
-- TOC entry 4183 (class 2606 OID 16431)
-- Name: monitor_records monitor_records_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.monitor_records
    ADD CONSTRAINT monitor_records_pkey PRIMARY KEY (id);


--
-- TOC entry 4181 (class 2606 OID 16423)
-- Name: websites websites_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.websites
    ADD CONSTRAINT websites_pkey PRIMARY KEY (id);


--
-- TOC entry 4184 (class 1259 OID 16437)
-- Name: site_id_index; Type: INDEX; Schema: public; Owner: avnadmin
--

CREATE INDEX site_id_index ON public.monitor_records USING btree (site_id);


--
-- TOC entry 4185 (class 2606 OID 16432)
-- Name: monitor_records monitor_record_website_id; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.monitor_records
    ADD CONSTRAINT monitor_record_website_id FOREIGN KEY (site_id) REFERENCES public.websites(id);


--
-- TOC entry 4330 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2023-01-14 12:50:53 CET

--
-- PostgreSQL database dump complete
--

