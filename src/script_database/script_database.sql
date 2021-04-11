# mysql -h localhost -u root -p
# abrir o MySQL ===> sudo mysql -u root -p

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
select id, sha1, date_time, is_merge_commit, id_project from commit;
select id, sha1, date_time, is_merge_commit, id_project from commit where sha1 = "3d52b53b46838d7ebe1d1a4258b88cde3dbaed65";
select id, id_commit, has_base_version, common_ancestor, extra_effort, wasted_effort, rework_effort  from merge_commit;
select id, type, id_commit from refactoring;
select * from merge_branch;

####### DATABASE ##############

drop database refactoring_merge;
create database if not exists refactoring_merge;
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
    extra_effort int,
    wasted_effort int,
    rework_effort int,
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