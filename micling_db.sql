--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: roleenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.roleenum AS ENUM (
    'usuario',
    'admin'
);


ALTER TYPE public.roleenum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: examenes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.examenes (
    id_examen integer NOT NULL,
    user_uid integer,
    user_name character varying,
    exam_type character varying,
    res_1 double precision,
    res_2 double precision,
    res_3 double precision,
    res_4 double precision,
    res_5 double precision,
    res_6 double precision,
    res_7 double precision,
    res_8 double precision,
    res_9 double precision,
    res_10 double precision,
    total_percentage double precision,
    creation_date timestamp without time zone
);


ALTER TABLE public.examenes OWNER TO postgres;

--
-- Name: examenes_id_examen_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.examenes_id_examen_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.examenes_id_examen_seq OWNER TO postgres;

--
-- Name: examenes_id_examen_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.examenes_id_examen_seq OWNED BY public.examenes.id_examen;


--
-- Name: exams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exams (
    id_examen integer NOT NULL,
    user_uid integer NOT NULL,
    user_name character varying(255) NOT NULL,
    exam_type character varying(50),
    res_1 text,
    res_2 text,
    res_3 text,
    res_4 text,
    res_5 text,
    res_6 text,
    res_7 text,
    res_8 text,
    res_9 text,
    res_10 text,
    total_percentage numeric,
    creation_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.exams OWNER TO postgres;

--
-- Name: exams_id_examen_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exams_id_examen_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exams_id_examen_seq OWNER TO postgres;

--
-- Name: exams_id_examen_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exams_id_examen_seq OWNED BY public.exams.id_examen;


--
-- Name: images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.images (
    id integer NOT NULL,
    url character varying NOT NULL,
    file_name character varying NOT NULL
);


ALTER TABLE public.images OWNER TO postgres;

--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.images_id_seq OWNER TO postgres;

--
-- Name: images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;


--
-- Name: refresh_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.refresh_tokens (
    token_uid integer NOT NULL,
    user_uid integer NOT NULL,
    refresh_token text NOT NULL,
    expires_at timestamp without time zone
);


ALTER TABLE public.refresh_tokens OWNER TO postgres;

--
-- Name: refresh_tokens_token_uid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.refresh_tokens_token_uid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.refresh_tokens_token_uid_seq OWNER TO postgres;

--
-- Name: refresh_tokens_token_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.refresh_tokens_token_uid_seq OWNED BY public.refresh_tokens.token_uid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_uid integer NOT NULL,
    username character varying(55) NOT NULL,
    last_name character varying(55) NOT NULL,
    password text NOT NULL,
    phone_number character varying,
    rol public.roleenum DEFAULT 'usuario'::public.roleenum,
    institucion character varying(70),
    grade character varying(20),
    creation_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    last_modified timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    country_origin character varying,
    language_skills jsonb,
    courses character varying[],
    age integer,
    gender character varying,
    email character varying(255),
    photo character varying(255)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_uid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_uid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_uid_seq OWNER TO postgres;

--
-- Name: users_user_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_uid_seq OWNED BY public.users.user_uid;


--
-- Name: examenes id_examen; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examenes ALTER COLUMN id_examen SET DEFAULT nextval('public.examenes_id_examen_seq'::regclass);


--
-- Name: exams id_examen; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exams ALTER COLUMN id_examen SET DEFAULT nextval('public.exams_id_examen_seq'::regclass);


--
-- Name: images id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);


--
-- Name: refresh_tokens token_uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens ALTER COLUMN token_uid SET DEFAULT nextval('public.refresh_tokens_token_uid_seq'::regclass);


--
-- Name: users user_uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_uid SET DEFAULT nextval('public.users_user_uid_seq'::regclass);


--
-- Data for Name: examenes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.examenes (id_examen, user_uid, user_name, exam_type, res_1, res_2, res_3, res_4, res_5, res_6, res_7, res_8, res_9, res_10, total_percentage, creation_date) FROM stdin;
\.


--
-- Data for Name: exams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exams (id_examen, user_uid, user_name, exam_type, res_1, res_2, res_3, res_4, res_5, res_6, res_7, res_8, res_9, res_10, total_percentage, creation_date) FROM stdin;
\.


--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.images (id, url, file_name) FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.refresh_tokens (token_uid, user_uid, refresh_token, expires_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_uid, username, last_name, password, phone_number, rol, institucion, grade, creation_date, last_modified, country_origin, language_skills, courses, age, gender, email, photo) FROM stdin;
\.


--
-- Name: examenes_id_examen_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.examenes_id_examen_seq', 5, true);


--
-- Name: exams_id_examen_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exams_id_examen_seq', 1, false);


--
-- Name: images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.images_id_seq', 1, false);


--
-- Name: refresh_tokens_token_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.refresh_tokens_token_uid_seq', 34, true);


--
-- Name: users_user_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_uid_seq', 51, true);


--
-- Name: examenes examenes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.examenes
    ADD CONSTRAINT examenes_pkey PRIMARY KEY (id_examen);


--
-- Name: exams exams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_pkey PRIMARY KEY (id_examen);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (token_uid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_uid);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_examenes_id_examen; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_examenes_id_examen ON public.examenes USING btree (id_examen);


--
-- Name: ix_examenes_user_uid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_examenes_user_uid ON public.examenes USING btree (user_uid);


--
-- Name: ix_images_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_images_id ON public.images USING btree (id);


--
-- Name: exams exams_user_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_user_uid_fkey FOREIGN KEY (user_uid) REFERENCES public.users(user_uid);


--
-- Name: refresh_tokens refresh_tokens_user_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_user_uid_fkey FOREIGN KEY (user_uid) REFERENCES public.users(user_uid) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

