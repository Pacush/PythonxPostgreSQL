PGDMP  4    '            	    |            NucleoDeDiagnostico    16.4    16.4     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16398    NucleoDeDiagnostico    DATABASE     �   CREATE DATABASE "NucleoDeDiagnostico" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
 %   DROP DATABASE "NucleoDeDiagnostico";
                postgres    false            �            1259    16415    doctores    TABLE     j  CREATE TABLE public.doctores (
    codigo integer NOT NULL,
    nombre character varying(50) NOT NULL,
    direccion character varying(50) NOT NULL,
    telefono character varying(15) NOT NULL,
    fecha_nac date NOT NULL,
    sexo character varying(10) NOT NULL,
    especialidad character varying(50) NOT NULL,
    contrasena character varying(20) NOT NULL
);
    DROP TABLE public.doctores;
       public         heap    postgres    false            �            1259    16409 	   empleados    TABLE     ?  CREATE TABLE public.empleados (
    codigo integer NOT NULL,
    nombre character varying(50),
    direccion character varying(50),
    telefono character varying(15),
    fecha_nac date,
    sexo character varying(10),
    sueldo numeric(10,2),
    turno character varying(10),
    contrasena character varying(20)
);
    DROP TABLE public.empleados;
       public         heap    postgres    false            �            1259    16406    empleados_codigo_seq    SEQUENCE     }   CREATE SEQUENCE public.empleados_codigo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.empleados_codigo_seq;
       public          postgres    false            �            1259    16422 	   pacientes    TABLE     J  CREATE TABLE public.pacientes (
    codigo integer NOT NULL,
    nombre character varying(50) NOT NULL,
    direccion character varying(50) NOT NULL,
    telefono character varying(15) NOT NULL,
    fecha_nac date NOT NULL,
    sexo character varying(10) NOT NULL,
    edad integer NOT NULL,
    estatura numeric(2,0) NOT NULL
);
    DROP TABLE public.pacientes;
       public         heap    postgres    false            �          0    16415    doctores 
   TABLE DATA           r   COPY public.doctores (codigo, nombre, direccion, telefono, fecha_nac, sexo, especialidad, contrasena) FROM stdin;
    public          postgres    false    217          �          0    16409 	   empleados 
   TABLE DATA           t   COPY public.empleados (codigo, nombre, direccion, telefono, fecha_nac, sexo, sueldo, turno, contrasena) FROM stdin;
    public          postgres    false    216   2       �          0    16422 	   pacientes 
   TABLE DATA           i   COPY public.pacientes (codigo, nombre, direccion, telefono, fecha_nac, sexo, edad, estatura) FROM stdin;
    public          postgres    false    218   �       �           0    0    empleados_codigo_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.empleados_codigo_seq', 5, true);
          public          postgres    false    215            [           2606    16419    doctores doctores_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.doctores
    ADD CONSTRAINT doctores_pkey PRIMARY KEY (codigo);
 @   ALTER TABLE ONLY public.doctores DROP CONSTRAINT doctores_pkey;
       public            postgres    false    217            Y           2606    16413    empleados empleados_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.empleados
    ADD CONSTRAINT empleados_pkey PRIMARY KEY (codigo);
 B   ALTER TABLE ONLY public.empleados DROP CONSTRAINT empleados_pkey;
       public            postgres    false    216            ]           2606    16426    pacientes pacientes_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_pkey PRIMARY KEY (codigo);
 B   ALTER TABLE ONLY public.pacientes DROP CONSTRAINT pacientes_pkey;
       public            postgres    false    218            �   !  x�M��n�0���S���&h��@���8��"�1J}�%e�8��?���2�>b\�8�H3|�+�]\�C&g�Dw�u��La"PR
���R���PvcZ�[ى#�!{X0M�+��ա�
]�ƈ����|�G
�(�6Fb/z����PFɍQ��P�U���c���땴�����Gx�n��n�s8�v�%�s�D��c=t������JV˺������Ha	B�a�Eg��@�˗�/��q�6�w���Q�+[��T�^4RɪQB*[4���9Sq�a�Y���WM����}�      �   �   x��A�0E��S���,�`�ݨ+7�LLI-q���_���_����zd��O��$><�Ow8@�_	z�{�QSS��XbA�u�ԸMf����XQNW��e���&�
a-<O��;�}d،�u_���R��5��,aWdf��m۵���+crWA�:_Ή8S$Q�r��)=6�      �   �   x�M��j�  ���)�,����ҟ�Ba鹗Iփ`Pr�>}-{���,|6�{��G���;ݫt�kK��rr��T��ۑ*�H`-��ޒ�A+�E�⾟%W��L.��*7����&W.����X�l�p�tP䞜���uK��M�gi���-�"�g��1�ef#�Ay��<���2���i�� ��A�     