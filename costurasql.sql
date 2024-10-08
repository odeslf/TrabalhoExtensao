PGDMP  /                    |            costura    16.3    16.3     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    41037    costura    DATABASE     ~   CREATE DATABASE costura WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Portuguese_Brazil.1252';
    DROP DATABASE costura;
                postgres    false            �            1259    41039    fabrica    TABLE     �   CREATE TABLE public.fabrica (
    id integer NOT NULL,
    nome character varying(255) NOT NULL,
    telefone character varying(15),
    endereco character varying(255) NOT NULL
);
    DROP TABLE public.fabrica;
       public         heap    postgres    false            �            1259    41038    fabrica_id_seq    SEQUENCE     �   CREATE SEQUENCE public.fabrica_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.fabrica_id_seq;
       public          postgres    false    216            �           0    0    fabrica_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.fabrica_id_seq OWNED BY public.fabrica.id;
          public          postgres    false    215            �            1259    41048    pedido    TABLE     �   CREATE TABLE public.pedido (
    id integer NOT NULL,
    fabrica_id integer,
    quantidade integer NOT NULL,
    preco_por_peca numeric(10,2) NOT NULL
);
    DROP TABLE public.pedido;
       public         heap    postgres    false            �            1259    41047    pedido_id_seq    SEQUENCE     �   CREATE SEQUENCE public.pedido_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.pedido_id_seq;
       public          postgres    false    218            �           0    0    pedido_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.pedido_id_seq OWNED BY public.pedido.id;
          public          postgres    false    217                       2604    41042 
   fabrica id    DEFAULT     h   ALTER TABLE ONLY public.fabrica ALTER COLUMN id SET DEFAULT nextval('public.fabrica_id_seq'::regclass);
 9   ALTER TABLE public.fabrica ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216                        2604    41051 	   pedido id    DEFAULT     f   ALTER TABLE ONLY public.pedido ALTER COLUMN id SET DEFAULT nextval('public.pedido_id_seq'::regclass);
 8   ALTER TABLE public.pedido ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    218    218            �          0    41039    fabrica 
   TABLE DATA           ?   COPY public.fabrica (id, nome, telefone, endereco) FROM stdin;
    public          postgres    false    216   m       �          0    41048    pedido 
   TABLE DATA           L   COPY public.pedido (id, fabrica_id, quantidade, preco_por_peca) FROM stdin;
    public          postgres    false    218          �           0    0    fabrica_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.fabrica_id_seq', 11, true);
          public          postgres    false    215            �           0    0    pedido_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.pedido_id_seq', 8, true);
          public          postgres    false    217            "           2606    41046    fabrica fabrica_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.fabrica
    ADD CONSTRAINT fabrica_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.fabrica DROP CONSTRAINT fabrica_pkey;
       public            postgres    false    216            $           2606    41053    pedido pedido_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.pedido
    ADD CONSTRAINT pedido_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.pedido DROP CONSTRAINT pedido_pkey;
       public            postgres    false    218            %           2606    41054    pedido pedido_fabrica_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.pedido
    ADD CONSTRAINT pedido_fabrica_id_fkey FOREIGN KEY (fabrica_id) REFERENCES public.fabrica(id);
 G   ALTER TABLE ONLY public.pedido DROP CONSTRAINT pedido_fabrica_id_fkey;
       public          postgres    false    4642    218    216            �   �   x�u���@D뽯�����+���Y�$�5����������r������`��κ�C;3^��HQ�7��Z�4Gƀ���<��w����'��#_��3��5o��H��_S�M�ѺL��7%"8�1��O���Ɠ����p��˶��n��z/G�      �   7   x�Uɱ 0���d�9B�_�n���d)&1�V��Q��pG-�x���:
�     