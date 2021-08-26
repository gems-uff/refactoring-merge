# mysql -h localhost -u root -p
# abrir o MySQL ===> sudo mysql -u root -p
# backup do bd
mysqldump -u root -p refactoring_merge > /mnt/c/Users/aoliv/refactoring-merge/output/backup_bd.sql


########### Dicas de quando dá uma travada no MySQL
This error occurs due to multiple installations of mysql. Run the command:

ps -A|grep mysql
sudo pkill mysql
ps -A|grep mysqld
sudo pkill mysqld
sudo service mysql restart
mysql -u root -p


##### Queries 

use refactoring_merge;

#### Listar todas as tuplas
select * from project;
select id, sha1, date_time, is_merge_commit, id_project, refminer_timeout from commit;
select id, sha1, date_time, is_merge_commit, id_project from commit where sha1 = "3d52b53b46838d7ebe1d1a4258b88cde3dbaed65";
select id, id_commit, is_fast_forward_merge, extra_effort, wasted_effort, rework_effort, branch1_actions, branch2_actions, merge_actions  from merge_commit;
select id, type, id_commit from refactoring;
select refactoring.type from refactoring, commit where refactoring.id_commit = commit.id and commit.sha1 = "7454526686afe3509e8472643beead42d1d4e24c";


select commit.id, id_commit, is_fast_forward_merge, extra_effort, wasted_effort, rework_effort, branch1_actions, branch2_actions, merge_actions  from merge_commit, commit, project where project.id = commit.id_project and commit.id = merge_commit.id_commit;

select count(*) from merge_commit where extra_effort > 0 or wasted_effort > 0 or rework_effort > 0;

"""retornar a quantidade de refactorings por TIPO """
select type, count(*) as qty from refactoring group by type order by qty desc;

"""retornar a quantidade de refactorings por id do projeto """
select refactoring.type, count(*) as qty from project, commit, refactoring where project.id = 2 and project.id = commit.id_project and commit.id = refactoring.id_commit group by type order by qty desc;

"""Selecionar da quantidade de refatorações por tipo por commit - via sha1"""
select refactoring.type, count(*) as qty from commit, refactoring where commit.sha1 = "2f21db0b434f6889caaa1550c6b35691065e3df5" and commit.id = refactoring.id_commit group by type order by qty desc;

"""Selecionar da quantidade de refatorações por tipo por commit - via id-commit"""
select refactoring.type, count(*) as qty from commit, refactoring where commit.id = 874 and commit.id = refactoring.id_commit group by type order by qty desc;

"""verificar se é um commit de merge"""
select is_merge_commit from commit where id = 120274;

"""Selecionar commits nos branches de um merge """
select merge_branch.id_merge_commit, (select commit.sha1 from commit where id = merge_branch.id_commit) as sha1, (select commit.date_time from commit where id = merge_branch.id_commit) as date_time , merge_branch.id_commit, merge_branch.type_branch from commit, merge_branch where commit.sha1 = "2f21db0b434f6889caaa1550c6b35691065e3df5" and commit.id = merge_branch.id_merge_commit;

select * from merge_branch;

ALTER TABLE merge_commit CHANGE extra_effort extra_effort bigint;
ALTER table commit add column refminer_timeout enum('False', 'True') DEFAULT 'False' NOT NULL after parent;








####### DATABASE ##############

use refactoring_merge;

create table project(
    id bigint AUTO_INCREMENT,
    name varchar(100) NOT NULL,
    path_workdir varchar(200) NOT NULL UNIQUE,
    url varchar(200),    
    PRIMARY KEY (id)
);

create table commit(
    id bigint AUTO_INCREMENT,
    sha1 varchar(40) NOT NULL,
    author varchar(100) NOT NULL,
    message varchar(500),
    commiter varchar(100) NOT NULL,
    date_time timestamp NOT NULL,  
    is_merge_commit enum('False', 'True') NOT NULL,
    parent varchar(40),
    refminer_timeout enum('False', 'True') DEFAULT 'False' NOT NULL,
    id_project bigint,
    PRIMARY KEY (id),
    FOREIGN KEY (id_project) REFERENCES project(id)
);

create table merge_commit(
    id bigint AUTO_INCREMENT,  
    has_base_version enum('False', 'True') NOT NULL,
    common_ancestor varchar(40) NOT NULL,
    parent1 varchar(40) NOT NULL,
    parent2 varchar(40) NOT NULL,
    is_fast_forward_merge enum('False', 'True') NOT NULL,
    extra_effort bigint,
    wasted_effort bigint,
    rework_effort bigint,
    branch1_actions bigint,
	branch2_actions bigint,
	merge_actions bigint,
    id_commit bigint,
    PRIMARY KEY (id),
    FOREIGN KEY (id_commit) REFERENCES commit(id)
);

create table merge_branch(
    id bigint AUTO_INCREMENT,
    id_commit bigint,
    id_merge_commit bigint,
    type_branch enum('1', '2') NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_commit) REFERENCES commit(id),
    FOREIGN KEY (id_merge_commit) REFERENCES commit(id)
);

create table refactoring(
    id bigint AUTO_INCREMENT,
    type varchar(100) NOT NULL,
    description varchar(1000) NOT NULL,
    id_commit bigint,  
    PRIMARY KEY (id),
    FOREIGN KEY (id_commit) REFERENCES commit(id)    
);









































drop database refactoring_merge;
drop database refactoring_merge_t;
create database if not exists refactoring_merge; 
create database if not exists refactoring_merge_t; 



"Deletar projeto - nesta ordem"
"tabela refactoring"
delete from refactoring where refactoring.id_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 30);
"tabela merge_branch"
delete from merge_branch where merge_branch.id_merge_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 30);
"tabela merge_commit"
delete from merge_commit where merge_commit.id_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 30);
"tabela commit"
delete from commit where id_project = 30;
"tabela projeto"
delete from project where id = 3;