CREATE TABLE public.user (
    id SERIAL NOT NULL,
    card_id varchar(16) NOT NULL,
    name varchar(64) NOT NULL,
    profile_id integer NOT NULL,
    notify_on_access boolean NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE public.user
    ADD UNIQUE (card_id);

CREATE INDEX ON public.user
    (profile_id);


CREATE TABLE public.history (
    id SERIAL NOT NULL,
    user_id integer,
    card_id varchar(16),
    created_at timestamp with time zone NOT NULL,
    access_granted boolean NOT NULL,
    PRIMARY KEY (id)
);

CREATE INDEX ON public.history
    (user_id);


CREATE TABLE public.profile (
    id SERIAL NOT NULL,
    name varchar NOT NULL,
    expire_at date,
    from_hour integer,
    to_hour integer,
    from_weekday integer,
    to_weekday integer,
    PRIMARY KEY (id)
);

ALTER TABLE public.profile
    ADD UNIQUE (name);


ALTER TABLE public.user ADD CONSTRAINT FK_user__profile_id FOREIGN KEY (profile_id) REFERENCES public.profile(id);
ALTER TABLE public.history ADD CONSTRAINT FK_history__user_id FOREIGN KEY (user_id) REFERENCES public.user(id);