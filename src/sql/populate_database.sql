-- Departamento

INSERT INTO departamento
(nome, codigo)
VALUES ('DEPTO Ciencia da Computação', 1),
       ('DEPTO Artes Visuais', 2),
       ('DEPTO Odontologia', 3);


-- Professores

INSERT INTO professor
(nome, matricula, departamento_codigo)
VALUES ('Jaozim', '1234', 1),
       ('Pedrim', '4321', 2),
       ('Juju', '2314', 3);


-- Disciplinas

INSERT INTO disciplina
(codigo, nome, departamento_codigo)
VALUES ('BD1234', 'Banco de Dados', 1),
       ('HA1234', 'Historia da Arte', 2),
       ('PD1234', 'Prótese Dentária', 1);


-- Turmas

INSERT INTO turma
(periodo, numero, horario, matricula_professor, codigo_disciplina)
VALUES ('01-2023', 1, '12:00', '1234', 'BD1234'),
       ('02-2023', 2, '23:59', '4321', 'HA1234'),
       ('01-2029', 2, '14:59', '2314', 'PD1234');

-- Estudantes

INSERT INTO estudante
(email, matricula, avatar, senha, admin)
VALUES ('20001234@aluno.unb.br', 20001234, 'avatar1', '1234', false),
       ('20004321@aluno.unb.br', 20004321, 'avatar2', '1234', false),
       ('20001423@aluno.unb.br', 20001423, 'avatar3', '1234', false),
       ('1@aluno.unb.br', 1, 'avatar4', 'admin', true);

-- Avaliações

INSERT INTO avaliacao
(estrelas, comentario, turma_periodo, turma_matricula_professor, turma_codigo_disciplina, estudante_matricula)
VALUES (2, 'Achei triste', '01-2023', '1234', 'BD1234', 20001234),
       (5, 'Achei daora', '01-2023', '1234', 'BD1234', 20004321),
       (1, 'Achei triste', '02-2023', '4321', 'HA1234', 20001234),
       (4, 'Achei Massa', '02-2023', '4321', 'HA1234', 20004321),
       (2, 'Achei triste', '01-2029', '2314', 'PD1234', 20001234),
       (5, 'Achei massa', '01-2029', '2314', 'PD1234', 20004321);


-- Denúncias

INSERT INTO denuncia
(comentario, avaliacao_turma_periodo, avaliacao_turma_matricula_professor, avaliacao_turma_codigo_disciplina, avaliacao_estudante_matricula, estudante_matricula)
VALUES ('Achei ofensivo', '01-2029', '2314', 'PD1234', 20004321, 20001234),
       ('Achei ofensivo', '02-2023', '4321', 'HA1234', 20004321, 20001234),
       ('Achei ofensivo', '01-2029', '2314', 'PD1234', 20001234, 20004321);
