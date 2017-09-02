-- clear all existing vehicle data
TRUNCATE vehicle CASCADE;
-- define list of vehicles known to the logging system
INSERT INTO vehicle 
  (id  , name   , description)
 VALUES
  (7   , 'E7'   , 'E0711-7'),
  (7000, 'E7000', 'E0711-7000 (E7 modified for Driverless Operation)'),
  (8   , 'E8'   , 'E0711-8');


-- clear all existing component data
TRUNCATE component CASCADE;
-- list of components 
INSERT INTO component 
  (id  , name  , description) 
 VALUES
  (1, 	'ObjectRecognition',	''),
  (2,	'Slam', 		''),
  (3,	'TrackRecognition', 	''),
  (4,	'TrajectoryPlanning', 	''),
  (6,	'Sensorfusion',	''),
  (8,	'Lidar', 		''),
  (9,	'Cam100Left', 		''),
  (10,	'Cam100Right',		''),
  (11,	'Cam60Left', 		''),
  (12,	'Cam60Right',		''),
  (13,  'ShortDistanceControl', '');


-- clear all existing msgtype data
TRUNCATE msgtype CASCADE;
-- define list of message types known to the logging system
INSERT INTO msgtype 
  (id  , shortname, name, description)
 VALUES
(1, 'Cones',			'ObjectRecognition_Cones',	'Object Recognition Cone List'),
(2, 'SlamMap',			'',				'Map output of SLAM Subsystem'),
(3, 'SortedMap',		'',				''),
(5, 'TrajectoryPlanning_1',	'',				''),
(6, 'VehicleStateDynamic',	'',				''),
(7, 'SlamPositionOrientation',	'',				''),
(8, 'LidarSegments',		'',				''),
(9, 'Cam100Left',		'', 				''),
(10, 'Cam100Right',		'',				''),
(11, 'Cam60Left',		'',				''),
(12, 'Cam60Right',		'',				''),
(13, 'FrameTrigger',    '',             ''),
(14, 'SDCParametersSimple',   '',             'Parameter for the simple short distance controller');




-- clear all existing vehicle_component_msgtype data
TRUNCATE vehicle_component_msgtype CASCADE;
-- defines the relation between components and msgtypes in each vehicle and holds live data for telemetry
INSERT INTO vehicle_component_msgtype
  (id, vehicle, component, msgtype, seqnr, lastdata, lasttlocal)
 VALUES
(1, 	7000, 1, 1, 0, NULL, NULL),				--Cones
(2, 	7000, 2, 2, 0, NULL, NULL),				--SlamMap
(3, 	7000, 3, 3, 0, NULL, NULL),				--SortedMap
(5, 	7000, 4, 5, 0, NULL, NULL),				--TrajectoryPlanning_1
(6, 	7000, 6, 6, 0, NULL, NULL),				--VehicleStateDynamic
(7, 	7000, 2, 7, 0, NULL, NULL),				--SlamPositionOrientation
(8,  	7000, 8, 8, 0, NULL, NULL),				--LidarSegments
(9,  	7000, 9, 9, 0, NULL, NULL),				--Cam100Left
(10, 	7000, 10, 10, 0, NULL, NULL),			--Cam100Right
(11,  	7000, 11, 11, 0, NULL, NULL),			--Cam60Left
(12, 	7000, 12, 12, 0, NULL, NULL),			--Cam60Right
(13,    7000,  1 , 13, 0, NULL, NULL);           --FrameTrigger
(14,    7000,  13, 14, 0, NULL, NULL);

SELECT run_new(7000, NULL, NULL, 'Regelungstests', 'Renningen');























