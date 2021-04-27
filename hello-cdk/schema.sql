DROP TABLE IF EXISTS  rooms, admins, room_admins, records, room_records;

-- rooms, admins, room_admins, records, room_records
CREATE TABLE rooms 
(
    id                INT GENERATED ALWAYS AS IDENTITY NOT NULL,
    room_number       TEXT NOT NULL,
    building_number   TEXT NOT NULL,
    max_capacity      INT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE admins
(
    id              INT GENERATED ALWAYS AS IDENTITY NOT NULL,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    department      TEXT NOT NULL,
    phone           TEXT NOT NULL,
    email           TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE room_admins
(
    room_id      INT NOT NULL,
    admin_id     INT NOT NULL,
    CONSTRAINT fk_room
        FOREIGN KEY(room_id)
            REFERENCES rooms(id),
    CONSTRAINT fk_admin
        FOREIGN KEY(admin_id)
            REFERENCES admins(id)
);

CREATE TABLE records
(
    id              INT GENERATED ALWAYS AS IDENTITY NOT NULL,
    record_date     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    num_occupants   INT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE room_records
(
    room_id      INT NOT NULL,
    record_id    INT NOT NULL,
    CONSTRAINT fk_room
        FOREIGN KEY(room_id)
            REFERENCES rooms(id),
    CONSTRAINT fk_record
        FOREIGN KEY(record_id)
            REFERENCES records(id)
);