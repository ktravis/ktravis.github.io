drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    title text not null,
    text text not null,
    slug text not null,
    timestamp date default (datetime('now', 'localtime')) not null
);
