CREATE TABLE IF NOT EXISTS  departamento (
	nome varchar NOT NULL,
	codigo int4 NOT NULL,
	CONSTRAINT departamento_pk PRIMARY KEY (codigo)
);


CREATE TABLE IF NOT EXISTS estudante (
	email varchar NOT NULL,
	matricula int4 NOT NULL,
	avatar bytea NULL,
	senha varchar NOT NULL,
	"admin" bool NOT NULL DEFAULT false,
	CONSTRAINT estudante_pk PRIMARY KEY (matricula)
);


CREATE TABLE IF NOT EXISTS disciplina (
	codigo varchar NOT NULL,
	nome varchar NOT NULL,
	departamento_codigo int4 NOT NULL,
	CONSTRAINT disciplina_pk PRIMARY KEY (codigo),
	CONSTRAINT disciplina_fk FOREIGN KEY (departamento_codigo) REFERENCES departamento(codigo)
);


CREATE TABLE IF NOT EXISTS professor (
	nome varchar NOT NULL,
	matricula varchar NOT NULL,
	departamento_codigo int4 NOT NULL,
	CONSTRAINT professor_pk PRIMARY KEY (matricula),
	CONSTRAINT departamento_fk FOREIGN KEY (departamento_codigo) REFERENCES departamento(codigo) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS turma (
	periodo varchar NOT NULL,
	numero int4 NOT NULL,
	horario varchar NOT NULL,
	matricula_professor varchar NOT NULL,
	codigo_disciplina varchar NOT NULL,
	CONSTRAINT turma_pk PRIMARY KEY (periodo, matricula_professor, codigo_disciplina),
	CONSTRAINT disciplina_fk FOREIGN KEY (codigo_disciplina) REFERENCES disciplina(codigo),
	CONSTRAINT professor_fk FOREIGN KEY (matricula_professor) REFERENCES professor(matricula)
);


CREATE TABLE IF NOT EXISTS avaliacao (
	estrelas int4 NOT NULL,
	comentario varchar NULL,
	turma_periodo varchar NOT NULL,
	turma_matricula_professor varchar NOT NULL,
	turma_codigo_disciplina varchar NOT NULL,
	estudante_matricula int4 NOT NULL,
	CONSTRAINT avaliacao_pk PRIMARY KEY (estudante_matricula, turma_codigo_disciplina, turma_matricula_professor, turma_periodo),
	CONSTRAINT estudante_fk FOREIGN KEY (estudante_matricula) REFERENCES estudante(matricula) ON DELETE CASCADE,
	CONSTRAINT turma_fk FOREIGN KEY (turma_periodo,turma_matricula_professor,turma_codigo_disciplina) REFERENCES turma(periodo,matricula_professor,codigo_disciplina) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS denuncia (
	comentario varchar NOT NULL,
	avaliacao_turma_periodo varchar NOT NULL,
	avaliacao_turma_matricula_professor varchar NOT NULL,
	avaliacao_turma_codigo_disciplina varchar NOT NULL,
	avaliacao_estudante_matricula int4 NOT NULL,
	estudante_matricula int4 NOT NULL,
	CONSTRAINT denuncia_pk PRIMARY KEY (avaliacao_turma_periodo, avaliacao_turma_matricula_professor, avaliacao_turma_codigo_disciplina, avaliacao_estudante_matricula, estudante_matricula),
	CONSTRAINT avaliacao_fk FOREIGN KEY (avaliacao_estudante_matricula,avaliacao_turma_codigo_disciplina,avaliacao_turma_matricula_professor,avaliacao_turma_periodo) REFERENCES avaliacao(estudante_matricula,turma_codigo_disciplina,turma_matricula_professor,turma_periodo),
	CONSTRAINT estudante_fk FOREIGN KEY (estudante_matricula) REFERENCES estudante(matricula) ON DELETE CASCADE
);


CREATE OR REPLACE VIEW public.turma_avaliacoes_view
AS SELECT t.periodo AS turma_periodo,
    p.nome AS professor_nome,
    avg(a.estrelas) AS avaliacao_media,
    t.matricula_professor,
    t.codigo_disciplina
   FROM turma t
     JOIN professor p ON t.matricula_professor::text = p.matricula::text
     LEFT JOIN avaliacao a ON t.periodo::text = a.turma_periodo::text AND t.matricula_professor::text = a.turma_matricula_professor::text AND t.codigo_disciplina::text = a.turma_codigo_disciplina::text
  GROUP BY t.periodo, p.nome, t.matricula_professor, t.codigo_disciplina;
