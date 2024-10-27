DANGER ################################## DROP DATABASE IF EXISTS db_refac_merge_os;

CREATE DATABASE IF NOT EXISTS db_refac_merge_os_big;
SHOW DATABASES;

use db_refac_merge_os_big;

create table project(
    id bigint AUTO_INCREMENT,
    name varchar(100) NOT NULL,
    path_workdir varchar(200) NOT NULL UNIQUE,
    date_time_ini_exec timestamp DEFAULT CURRENT_TIMESTAMP,
    date_time_end_exec timestamp,
    number_commits bigint,
    number_merge_commits bigint,
    number_valid_merge_commits bigint,
    number_commits_refminer bigint,
    exec_script_branches enum('False', 'True') DEFAULT 'False' NOT NULL,
    exec_script_refactorings enum('False', 'True') DEFAULT 'False' NOT NULL,    
    exec_script_merge_effort enum('False', 'True') DEFAULT 'False' NOT NULL,
    selected_experiments enum('False', 'True') DEFAULT 'True' NOT NULL,
    url varchar(200),    
    PRIMARY KEY (id)
);

create table commit(
    id bigint AUTO_INCREMENT,
    sha1 varchar(40) NOT NULL UNIQUE,
    author varchar(200) NOT NULL,
    message varchar(500),
    commiter varchar(100) NOT NULL,
    date_time timestamp NOT NULL,  
    is_merge_commit enum('False', 'True') NOT NULL,
    parent varchar(40),
    refminer_execute enum('False', 'True') DEFAULT 'False' NOT NULL,
    refminer_timeout enum('False', 'True') DEFAULT 'False' NOT NULL,
    id_project bigint,
    PRIMARY KEY (id),
    FOREIGN KEY (id_project) REFERENCES project(id)
);

create table merge_commit(
    id bigint AUTO_INCREMENT,  
    has_base_version enum('False', 'True') NOT NULL,
    isPullRequest enum('False', 'True') DEFAULT 'False' NOT NULL,
    common_ancestor varchar(40) NOT NULL,
    common_ancestor_date_time timestamp, 
    parent1 varchar(40) NOT NULL,
    parent2 varchar(40) NOT NULL,
    is_fast_forward_merge enum('False', 'True') NOT NULL,
    merge_effort_calculated enum('False', 'True') DEFAULT 'False' NOT NULL,
    merge_effort_calc_timeout enum('False', 'True') DEFAULT 'True' NOT NULL,
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
    leftSideLocations json,
    rightSideLocations json,
    id_commit bigint,  
    PRIMARY KEY (id),
    FOREIGN KEY (id_commit) REFERENCES commit(id)    
);

create table refac_accept_type(    
    type varchar(100) NOT NULL UNIQUE    
);

INSERT INTO refac_accept_type (type) VALUES ('Change Parameter Type');
INSERT INTO refac_accept_type (type) VALUES ('Change Return Type');
INSERT INTO refac_accept_type (type) VALUES ('Change Variable Type');
INSERT INTO refac_accept_type (type) VALUES ('Extract Attribute');
INSERT INTO refac_accept_type (type) VALUES ('Extract Class');
INSERT INTO refac_accept_type (type) VALUES ('Extract Interface');
INSERT INTO refac_accept_type (type) VALUES ('Extract Method');
INSERT INTO refac_accept_type (type) VALUES ('Extract Subclass');
INSERT INTO refac_accept_type (type) VALUES ('Extract Superclass');
INSERT INTO refac_accept_type (type) VALUES ('Extract Variable');
INSERT INTO refac_accept_type (type) VALUES ('Inline Method');
INSERT INTO refac_accept_type (type) VALUES ('Inline Variable');
INSERT INTO refac_accept_type (type) VALUES ('Merge Attribute');
INSERT INTO refac_accept_type (type) VALUES ('Merge Parameter');
INSERT INTO refac_accept_type (type) VALUES ('Merge Variable');
INSERT INTO refac_accept_type (type) VALUES ('Move Attribute');
INSERT INTO refac_accept_type (type) VALUES ('Move Class');
INSERT INTO refac_accept_type (type) VALUES ('Move Method');
INSERT INTO refac_accept_type (type) VALUES ('Parameterize Variable');
INSERT INTO refac_accept_type (type) VALUES ('Pull Up Attribute');
INSERT INTO refac_accept_type (type) VALUES ('Pull Up Method');
INSERT INTO refac_accept_type (type) VALUES ('Push Down Attribute');
INSERT INTO refac_accept_type (type) VALUES ('Push Down Method');
INSERT INTO refac_accept_type (type) VALUES ('Rename Attribute');
INSERT INTO refac_accept_type (type) VALUES ('Rename Class');
INSERT INTO refac_accept_type (type) VALUES ('Rename Method');
INSERT INTO refac_accept_type (type) VALUES ('Rename Parameter');
INSERT INTO refac_accept_type (type) VALUES ('Rename Variable');
INSERT INTO refac_accept_type (type) VALUES ('Replace Attribute');
INSERT INTO refac_accept_type (type) VALUES ('Replace Variable With Attribute');
INSERT INTO refac_accept_type (type) VALUES ('Split Attribute');
INSERT INTO refac_accept_type (type) VALUES ('Split Parameter');
INSERT INTO refac_accept_type (type) VALUES ('Split Variable');





