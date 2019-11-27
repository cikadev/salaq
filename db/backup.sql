PGDMP         2            
    w            salaq    10.10    10.10 X    X           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            Y           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            Z           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            [           1262    16393    salaq    DATABASE     �   CREATE DATABASE salaq WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'English_United States.1252' LC_CTYPE = 'English_United States.1252';
    DROP DATABASE salaq;
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            \           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            ]           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    16527 
   discussion    TABLE     �   CREATE TABLE public.discussion (
    id integer NOT NULL,
    product_id integer NOT NULL,
    name character varying,
    content character varying
);
    DROP TABLE public.discussion;
       public         postgres    false    3            �            1259    16523    discussion_id_seq    SEQUENCE     �   CREATE SEQUENCE public.discussion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.discussion_id_seq;
       public       postgres    false    3    212            ^           0    0    discussion_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.discussion_id_seq OWNED BY public.discussion.id;
            public       postgres    false    210            �            1259    16525    discussion_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.discussion_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.discussion_product_id_seq;
       public       postgres    false    212    3            _           0    0    discussion_product_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.discussion_product_id_seq OWNED BY public.discussion.product_id;
            public       postgres    false    211            �            1259    16435    line    TABLE       CREATE TABLE public.line (
    id integer NOT NULL,
    user_email character varying NOT NULL,
    date date NOT NULL,
    ship_address text NOT NULL,
    postal_code character varying NOT NULL,
    note text,
    courrier_type character varying NOT NULL
);
    DROP TABLE public.line;
       public         postgres    false    3            �            1259    16438    line_id_seq    SEQUENCE     �   CREATE SEQUENCE public.line_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.line_id_seq;
       public       postgres    false    199    3            `           0    0    line_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.line_id_seq OWNED BY public.line.id;
            public       postgres    false    200            �            1259    16489    media    TABLE     �   CREATE TABLE public.media (
    id integer NOT NULL,
    type character varying NOT NULL,
    url character varying NOT NULL,
    product_id integer NOT NULL
);
    DROP TABLE public.media;
       public         postgres    false    3            �            1259    16485    media_id_seq    SEQUENCE     �   CREATE SEQUENCE public.media_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.media_id_seq;
       public       postgres    false    206    3            a           0    0    media_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.media_id_seq OWNED BY public.media.id;
            public       postgres    false    204            �            1259    16487    media_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.media_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.media_product_id_seq;
       public       postgres    false    3    206            b           0    0    media_product_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.media_product_id_seq OWNED BY public.media.product_id;
            public       postgres    false    205            �            1259    16470    product    TABLE     �   CREATE TABLE public.product (
    shop_id integer NOT NULL,
    id integer NOT NULL,
    title character varying,
    description text,
    price integer
);
    DROP TABLE public.product;
       public         postgres    false    3            �            1259    16468    product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.product_id_seq;
       public       postgres    false    203    3            c           0    0    product_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;
            public       postgres    false    202            �            1259    16466    product_shop_id_seq    SEQUENCE     �   CREATE SEQUENCE public.product_shop_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.product_shop_id_seq;
       public       postgres    false    203    3            d           0    0    product_shop_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.product_shop_id_seq OWNED BY public.product.shop_id;
            public       postgres    false    201            �            1259    16546    reply    TABLE     v   CREATE TABLE public.reply (
    parent_discussion_id integer NOT NULL,
    children_discussion_id integer NOT NULL
);
    DROP TABLE public.reply;
       public         postgres    false    3            �            1259    16544     reply_children_discussion_id_seq    SEQUENCE     �   CREATE SEQUENCE public.reply_children_discussion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.reply_children_discussion_id_seq;
       public       postgres    false    3    215            e           0    0     reply_children_discussion_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.reply_children_discussion_id_seq OWNED BY public.reply.children_discussion_id;
            public       postgres    false    214            �            1259    16542    reply_parent_discussion_id_seq    SEQUENCE     �   CREATE SEQUENCE public.reply_parent_discussion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.reply_parent_discussion_id_seq;
       public       postgres    false    215    3            f           0    0    reply_parent_discussion_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.reply_parent_discussion_id_seq OWNED BY public.reply.parent_discussion_id;
            public       postgres    false    213            �            1259    16410    shop    TABLE     �   CREATE TABLE public.shop (
    user_email character varying NOT NULL,
    name character varying NOT NULL,
    id integer NOT NULL
);
    DROP TABLE public.shop;
       public         postgres    false    3            �            1259    16416    shop_id_seq    SEQUENCE     �   CREATE SEQUENCE public.shop_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.shop_id_seq;
       public       postgres    false    3    196            g           0    0    shop_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.shop_id_seq OWNED BY public.shop.id;
            public       postgres    false    197            �            1259    16508    transaction    TABLE     c   CREATE TABLE public.transaction (
    line_id integer NOT NULL,
    product_id integer NOT NULL
);
    DROP TABLE public.transaction;
       public         postgres    false    3            �            1259    16504    transaction_line_id_seq    SEQUENCE     �   CREATE SEQUENCE public.transaction_line_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.transaction_line_id_seq;
       public       postgres    false    3    209            h           0    0    transaction_line_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.transaction_line_id_seq OWNED BY public.transaction.line_id;
            public       postgres    false    207            �            1259    16506    transaction_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.transaction_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.transaction_product_id_seq;
       public       postgres    false    3    209            i           0    0    transaction_product_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.transaction_product_id_seq OWNED BY public.transaction.product_id;
            public       postgres    false    208            �            1259    16418    users    TABLE     �   CREATE TABLE public.users (
    email character varying NOT NULL,
    password character varying,
    name character varying,
    balance integer DEFAULT 0 NOT NULL
);
    DROP TABLE public.users;
       public         postgres    false    3            �
           2604    16530    discussion id    DEFAULT     n   ALTER TABLE ONLY public.discussion ALTER COLUMN id SET DEFAULT nextval('public.discussion_id_seq'::regclass);
 <   ALTER TABLE public.discussion ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    210    212    212            �
           2604    16531    discussion product_id    DEFAULT     ~   ALTER TABLE ONLY public.discussion ALTER COLUMN product_id SET DEFAULT nextval('public.discussion_product_id_seq'::regclass);
 D   ALTER TABLE public.discussion ALTER COLUMN product_id DROP DEFAULT;
       public       postgres    false    211    212    212            �
           2604    16440    line id    DEFAULT     b   ALTER TABLE ONLY public.line ALTER COLUMN id SET DEFAULT nextval('public.line_id_seq'::regclass);
 6   ALTER TABLE public.line ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    200    199            �
           2604    16492    media id    DEFAULT     d   ALTER TABLE ONLY public.media ALTER COLUMN id SET DEFAULT nextval('public.media_id_seq'::regclass);
 7   ALTER TABLE public.media ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    206    204    206            �
           2604    16493    media product_id    DEFAULT     t   ALTER TABLE ONLY public.media ALTER COLUMN product_id SET DEFAULT nextval('public.media_product_id_seq'::regclass);
 ?   ALTER TABLE public.media ALTER COLUMN product_id DROP DEFAULT;
       public       postgres    false    205    206    206            �
           2604    16473    product shop_id    DEFAULT     r   ALTER TABLE ONLY public.product ALTER COLUMN shop_id SET DEFAULT nextval('public.product_shop_id_seq'::regclass);
 >   ALTER TABLE public.product ALTER COLUMN shop_id DROP DEFAULT;
       public       postgres    false    203    201    203            �
           2604    16474 
   product id    DEFAULT     h   ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);
 9   ALTER TABLE public.product ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    203    202    203            �
           2604    16549    reply parent_discussion_id    DEFAULT     �   ALTER TABLE ONLY public.reply ALTER COLUMN parent_discussion_id SET DEFAULT nextval('public.reply_parent_discussion_id_seq'::regclass);
 I   ALTER TABLE public.reply ALTER COLUMN parent_discussion_id DROP DEFAULT;
       public       postgres    false    215    213    215            �
           2604    16550    reply children_discussion_id    DEFAULT     �   ALTER TABLE ONLY public.reply ALTER COLUMN children_discussion_id SET DEFAULT nextval('public.reply_children_discussion_id_seq'::regclass);
 K   ALTER TABLE public.reply ALTER COLUMN children_discussion_id DROP DEFAULT;
       public       postgres    false    215    214    215            �
           2604    16425    shop id    DEFAULT     b   ALTER TABLE ONLY public.shop ALTER COLUMN id SET DEFAULT nextval('public.shop_id_seq'::regclass);
 6   ALTER TABLE public.shop ALTER COLUMN id DROP DEFAULT;
       public       postgres    false    197    196            �
           2604    16511    transaction line_id    DEFAULT     z   ALTER TABLE ONLY public.transaction ALTER COLUMN line_id SET DEFAULT nextval('public.transaction_line_id_seq'::regclass);
 B   ALTER TABLE public.transaction ALTER COLUMN line_id DROP DEFAULT;
       public       postgres    false    207    209    209            �
           2604    16512    transaction product_id    DEFAULT     �   ALTER TABLE ONLY public.transaction ALTER COLUMN product_id SET DEFAULT nextval('public.transaction_product_id_seq'::regclass);
 E   ALTER TABLE public.transaction ALTER COLUMN product_id DROP DEFAULT;
       public       postgres    false    208    209    209            R          0    16527 
   discussion 
   TABLE DATA               C   COPY public.discussion (id, product_id, name, content) FROM stdin;
    public       postgres    false    212   /^       E          0    16435    line 
   TABLE DATA               d   COPY public.line (id, user_email, date, ship_address, postal_code, note, courrier_type) FROM stdin;
    public       postgres    false    199   L^       L          0    16489    media 
   TABLE DATA               :   COPY public.media (id, type, url, product_id) FROM stdin;
    public       postgres    false    206   i^       I          0    16470    product 
   TABLE DATA               I   COPY public.product (shop_id, id, title, description, price) FROM stdin;
    public       postgres    false    203   �^       U          0    16546    reply 
   TABLE DATA               M   COPY public.reply (parent_discussion_id, children_discussion_id) FROM stdin;
    public       postgres    false    215   �^       B          0    16410    shop 
   TABLE DATA               4   COPY public.shop (user_email, name, id) FROM stdin;
    public       postgres    false    196   �^       O          0    16508    transaction 
   TABLE DATA               :   COPY public.transaction (line_id, product_id) FROM stdin;
    public       postgres    false    209   �^       D          0    16418    users 
   TABLE DATA               ?   COPY public.users (email, password, name, balance) FROM stdin;
    public       postgres    false    198   �^       j           0    0    discussion_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.discussion_id_seq', 1, false);
            public       postgres    false    210            k           0    0    discussion_product_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.discussion_product_id_seq', 1, false);
            public       postgres    false    211            l           0    0    line_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.line_id_seq', 1, false);
            public       postgres    false    200            m           0    0    media_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.media_id_seq', 1, false);
            public       postgres    false    204            n           0    0    media_product_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.media_product_id_seq', 1, false);
            public       postgres    false    205            o           0    0    product_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.product_id_seq', 1, false);
            public       postgres    false    202            p           0    0    product_shop_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.product_shop_id_seq', 1, false);
            public       postgres    false    201            q           0    0     reply_children_discussion_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.reply_children_discussion_id_seq', 1, false);
            public       postgres    false    214            r           0    0    reply_parent_discussion_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.reply_parent_discussion_id_seq', 1, false);
            public       postgres    false    213            s           0    0    shop_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.shop_id_seq', 1, false);
            public       postgres    false    197            t           0    0    transaction_line_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.transaction_line_id_seq', 1, false);
            public       postgres    false    207            u           0    0    transaction_product_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.transaction_product_id_seq', 1, false);
            public       postgres    false    208            �
           2606    16536    discussion discussion_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.discussion
    ADD CONSTRAINT discussion_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.discussion DROP CONSTRAINT discussion_pkey;
       public         postgres    false    212            �
           2606    16445    line line_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.line
    ADD CONSTRAINT line_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.line DROP CONSTRAINT line_pkey;
       public         postgres    false    199            �
           2606    16498    media media_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.media
    ADD CONSTRAINT media_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.media DROP CONSTRAINT media_pkey;
       public         postgres    false    206            �
           2606    16479    product product_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.product DROP CONSTRAINT product_pkey;
       public         postgres    false    203            �
           2606    16427    shop shop_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.shop
    ADD CONSTRAINT shop_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.shop DROP CONSTRAINT shop_pkey;
       public         postgres    false    196            �
           2606    16429    users user_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (email);
 9   ALTER TABLE ONLY public.users DROP CONSTRAINT user_pkey;
       public         postgres    false    198            �
           1259    16465    fki_line_fkey_user_email    INDEX     O   CREATE INDEX fki_line_fkey_user_email ON public.line USING btree (user_email);
 ,   DROP INDEX public.fki_line_fkey_user_email;
       public         postgres    false    199            �
           1259    16454    fki_shop_fkey_user_email    INDEX     O   CREATE INDEX fki_shop_fkey_user_email ON public.shop USING btree (user_email);
 ,   DROP INDEX public.fki_shop_fkey_user_email;
       public         postgres    false    196            �
           2606    16460    line line_fkey_user_email    FK CONSTRAINT     ~   ALTER TABLE ONLY public.line
    ADD CONSTRAINT line_fkey_user_email FOREIGN KEY (user_email) REFERENCES public.users(email);
 C   ALTER TABLE ONLY public.line DROP CONSTRAINT line_fkey_user_email;
       public       postgres    false    2743    199    198            �
           2606    16518    transaction line_id    FK CONSTRAINT     q   ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT line_id FOREIGN KEY (line_id) REFERENCES public.line(id);
 =   ALTER TABLE ONLY public.transaction DROP CONSTRAINT line_id;
       public       postgres    false    2746    199    209            �
           2606    16499    media product_id    FK CONSTRAINT     t   ALTER TABLE ONLY public.media
    ADD CONSTRAINT product_id FOREIGN KEY (product_id) REFERENCES public.product(id);
 :   ALTER TABLE ONLY public.media DROP CONSTRAINT product_id;
       public       postgres    false    203    2748    206            �
           2606    16513    transaction product_id    FK CONSTRAINT     z   ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT product_id FOREIGN KEY (product_id) REFERENCES public.product(id);
 @   ALTER TABLE ONLY public.transaction DROP CONSTRAINT product_id;
       public       postgres    false    203    2748    209            �
           2606    16537    discussion product_id    FK CONSTRAINT     y   ALTER TABLE ONLY public.discussion
    ADD CONSTRAINT product_id FOREIGN KEY (product_id) REFERENCES public.product(id);
 ?   ALTER TABLE ONLY public.discussion DROP CONSTRAINT product_id;
       public       postgres    false    2748    212    203            �
           2606    16449    shop shop_fkey_user_email    FK CONSTRAINT     ~   ALTER TABLE ONLY public.shop
    ADD CONSTRAINT shop_fkey_user_email FOREIGN KEY (user_email) REFERENCES public.users(email);
 C   ALTER TABLE ONLY public.shop DROP CONSTRAINT shop_fkey_user_email;
       public       postgres    false    196    2743    198            �
           2606    16455    line shop_fkey_user_email    FK CONSTRAINT     ~   ALTER TABLE ONLY public.line
    ADD CONSTRAINT shop_fkey_user_email FOREIGN KEY (user_email) REFERENCES public.users(email);
 C   ALTER TABLE ONLY public.line DROP CONSTRAINT shop_fkey_user_email;
       public       postgres    false    199    198    2743            �
           2606    16480    product shop_id    FK CONSTRAINT     m   ALTER TABLE ONLY public.product
    ADD CONSTRAINT shop_id FOREIGN KEY (shop_id) REFERENCES public.shop(id);
 9   ALTER TABLE ONLY public.product DROP CONSTRAINT shop_id;
       public       postgres    false    203    196    2741            R      x������ � �      E      x������ � �      L      x������ � �      I      x������ � �      U      x������ � �      B      x������ � �      O      x������ � �      D   A   x�K�K)J�K�+I,��.NtH�M���K���L�srp%���������?��=... �).     