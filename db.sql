create table Food (
    id integer primary key autoincrement,
    type integer default 0,
    subtype integer default 0,
    name text default "Unnamed food :^)",
    calories float default 0.0
);
