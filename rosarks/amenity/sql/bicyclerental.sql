BEGIN;
DROP TABLE IF EXISTS "amenity_bicyclerental" ;
CREATE TABLE "amenity_bicyclerental" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(30),
    "operator" varchar(30),
    "capacity" integer,
    "tags" varchar(3000) NOT NULL,
    "date_import" timestamp with time zone NOT NULL
)
;
SELECT AddGeometryColumn('amenity_bicyclerental', 'position', 4326, 'POINT', 2);
ALTER TABLE "amenity_bicyclerental" ALTER "position" SET NOT NULL;
CREATE INDEX "amenity_bicyclerental_position_id" ON "amenity_bicyclerental" USING GIST ( "position" );
COMMIT;
