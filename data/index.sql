--
--
CREATE INDEX "amenity_bicyclerental_position_id" ON "amenity_bicyclerental" USING GIST ( "position" );
--
--
CREATE INDEX "amenity_subwayroute_position_id" ON "amenity_bicyclerental" USING GIST ( "position" );
CREATE INDEX "amenity_subwaystation_position_id" ON "amenity_bicyclerental" USING GIST ( "position" );
--
--
CREATE INDEX "amenity_busstop_position_id" ON "amenity_bicyclerental" USING GIST ( "position" );
--
--
CREATE INDEX "amenity_tramroute_position_id" ON "amenity_bicyclerental" USING GIST ( "position" );
CREATE INDEX "amenity_tramstation_position_id" ON "amenity_bicyclerental" USING GIST ( "position" );