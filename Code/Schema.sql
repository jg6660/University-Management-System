drop table if exists Pay;
drop table if exists Rooms_have;
drop table if exists Live;
drop table if exists Taught;
drop table if exists Apply_to;
drop table if exists Payments;
drop table if exists Enroll;
drop table if exists Send_To;
drop table if exists Admins_employ;
drop table if exists Employs;
drop table if exists Professors;
drop table if exists Requests;
drop table if exists Classes_located;
drop table if exists Students;
drop table if exists Buildings_belong_to;
drop table if exists Schools_partof;
drop table if exists Dorms;
drop table if exists Universities;


create table Students (
    sid integer primary key,
    sfirst varchar(128),
    slast varchar(128),
    phno char(10),
    email varchar(64),
    address varchar(512),
    dob date,
    dept varchar(32),
    program_type varchar(32)
);

create table Professors(
    pid integer primary key,
    pfirst varchar(128),
    plast varchar(128),
    phno char(10),
    email varchar(64),
    address varchar(512),
    dob date,
    dept varchar(32)
);

create table Payments(
    payid serial primary key,
    term varchar(10),
    amount decimal,
    sid integer not null,
    foreign key( sid ) references Students( sid )
);

create table Universities(
    name varchar(128) primary key,
    address varchar(128),
    pincode integer,
    chancellor varchar(128)
);

create table Schools_partof(
    name varchar(128) primary key,
    address varchar(128),
    pincode integer,
    dean varchar(128),
    uname varchar(128) not null,
    foreign key(uname) references Universities(name)
);

create table Buildings_belong_to(
    name varchar(32) primary key,
    address varchar(128),
    pincode integer,
    no_of_rooms integer,
    schoolname varchar(32) not null,
    foreign key(schoolname) references Schools_partof(name)
);

create table Classes_located (
    cid varchar(32) primary key,
    cname varchar(128),
    day varchar(32),
    time time,
    dept varchar(32),
    bname varchar(32) not null,
    foreign key(bname) references Buildings_belong_to(name) 
);

create table Requests(
    rid serial primary key,
    category varchar(32),
    description varchar(128),
    sid integer not null,
    status varchar(16),
    prof_id integer,
    foreign key( sid ) references Students( sid )
);

create table Dorms (
    name varchar(32) primary key,
    address varchar(128),
    pincode integer,
    warden varchar(32)
);

create table Rooms_have(
    rno integer,
    floor integer,
    No_of_occupants integer,
    dname varchar(32),
    primary key(rno,dname),
    foreign key(dname) references Dorms(name) on delete cascade
);


create table Admins_employ(
    aid integer primary key,
    afirst varchar(128),
    alast varchar(128),
    aphno char(10),
    aemail varchar(64),
    address varchar(512),
    dob date,
    uname varchar(32) not null,
    foreign key(uname) references Universities(name)
);

create table Send_To(
    pid integer,
    rid integer,
    primary key(pid,rid),
    foreign key (pid) references Professors(pid),
    foreign key (rid) references Requests(rid)
);

create table Enroll(
    sid integer,
    cid varchar(32),
    primary key (sid, cid),
    foreign key(sid) references Students(sid),
    foreign key(cid) references Classes_located(cid)
);

create table Live(
    sid integer,
    dname varchar(32),
    primary key(sid, dname),
    foreign key(sid) references Students(sid),
    foreign key(dname) references Dorms(name)
);

create table Taught(
    cid varchar(32),
    pid integer,
    primary key(cid, pid),
    foreign key(cid) references Classes_located(cid),
    foreign key(pid) references Professors(pid)
);

create table Apply_to(
    sid integer,
    sname varchar(32),
    primary key(sid, sname),
    foreign key(sid) references Students(sid),
    foreign key(sname) references Schools_partof(name)
);

create table Employs(
    pid integer,
    sname varchar(32),
    primary key(pid, sname),
    foreign key(pid) references Professors(pid),
    foreign key(sname) references Schools_partof(name)
    
);

create table Pay(
    pid integer,
    aid integer,
    amount integer,
    dates date,
    primary key(pid, aid, dates),
    foreign key(pid) references Professors(pid),
    foreign key(aid) references Admins_employ(aid)
);

alter sequence requests_rid_seq restart with 500;
alter sequence payments_pid_seq restart with 500;









