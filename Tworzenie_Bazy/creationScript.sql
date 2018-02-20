-- Table: public.station_info

--helloworld.cggjgttkvbq5.eu-central-1.rds.amazonaws.com

-- DROP TABLE public.station_info;

-- Table: public.final_table

-- DROP TABLE public.final_table;

CREATE TABLE public.final_table
(
  index integer NOT NULL,
  temperatura text,
  cisnienie text,
  predkosc_wiatru text,
  wilgotnosc text,
  kierunek_wiatru text,
  warunki_pogodowe text,
  date timestamp without time zone,
  pm10 double precision,
  pm25 double precision,
  id_stacji integer,
  CONSTRAINT pk_key PRIMARY KEY (index),
  CONSTRAINT fk FOREIGN KEY (id_stacji)
      REFERENCES public.station_info (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk FOREIGN KEY (id_stacji)
      REFERENCES public.station_info (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.final_table
  OWNER TO postgres;

-- Index: public.ix_final_table_index
  
  
 -- Table: public.final_table

-- DROP TABLE public.final_table;

CREATE TABLE public.station_info
(
  id integer NOT NULL,
  nazwa_miejscowosci character varying(30),
  nazwa_ulicy character varying(60),
  szerokosc_stopnie double precision,
  szerokosc_minuty double precision,
  szerokosc_sekundy double precision,
  dlugosc_stopnie double precision,
  dlugosc_minuty double precision,
  dlugosc_sekundy double precision,
  liczba_glosow integer,
  biezaca_ocena double precision,
  CONSTRAINT station_info_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.station_info
  OWNER TO postgres;
