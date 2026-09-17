
-- 1-Which parking has the highest occupancy rate?
SELECT
    name,
    total,
    free,
    ROUND(
        ((total - free)::numeric / total) * 100,
        2
    ) AS occupancy_rate
FROM parking_locations
WHERE free IS NOT NULL
ORDER BY occupancy_rate DESC
LIMIT 1;
--2-Which parking location has the most free spaces
SELECT
    name,
    free
FROM parking_locations
WHERE free IS NOT NULL
ORDER BY free DESC
LIMIT 1;
--3-What is the average occupancy rate across active parking locations?
SELECT
    ROUND(
        AVG(((total - free)::numeric / total) * 100),
        2
    ) AS average_occupancy_rate
FROM parking_locations
WHERE free IS NOT NULL;
--4-Which parking locations have missing availability?
SELECT
    name,
    status,
    free
FROM parking_locations
WHERE free IS NULL;
--5-Which parking has the largest total capacity?
SELECT
    name,
    total
FROM parking_locations
ORDER BY total DESC
LIMIT 1;
--6- What is the average number of free spaces across all active parking locations?
SELECT
    ROUND(AVG(free), 2) AS average_free_spaces
FROM parking_locations
WHERE status = 1
AND free IS NOT NULL;

--7- What is the average occupancy rate across all parking locations
SELECT
    ROUND(
        AVG(((total - free)::numeric / total) * 100),
        2
    ) AS average_occupancy_rate
FROM parking_locations
WHERE free IS NOT NULL
AND total > 0;
-- 8-How many parking locations are active and how many are inactive?
SELECT
    status,
    COUNT(*) AS number_of_parkings
FROM parking_locations
GROUP BY status;
-- 9-Which parking locations are more than 80% occupied?
SELECT
    name,
    total,
    free,
    ROUND(
        ((total - free)::numeric / total) * 100,
        2
		
    ) AS occupancy_rate
FROM parking_locations
WHERE free IS NOT NULL
AND total > 0
AND ((total - free)::numeric / total) * 100 > 80
ORDER BY occupancy_rate DESC;


--10 What is the total parking capacity and
-- total number of free spaces across Turin?
SELECT
    SUM(total) AS total_parking_capacity,
    SUM(free) AS total_free_spaces
FROM parking_locations;

--TRAFFIC--
--1--- Which traffic measurement point has the highest flow?
SELECT
    sensor_id,
    road_name,
    direction,
    "offset",
    flow,
    speed
FROM traffic_locations
ORDER BY flow DESC
LIMIT 1;
--2- Which traffic measurement point has the lowest non-zero speed?
SELECT
    sensor_id,
    road_name,
    direction,
    "offset",
    speed,
    flow
FROM traffic_locations
WHERE speed > 0
ORDER BY speed ASC
LIMIT 1;
--3- Which roads have the highest traffic flow?
SELECT
    road_name,
    SUM(flow) AS total_flow
FROM traffic_locations
GROUP BY road_name
ORDER BY total_flow DESC
LIMIT 10;
--4- What is the average traffic flow across all measurement points?
SELECT
    ROUND(AVG(flow), 2) AS average_traffic_flow
FROM traffic_locations;
--5- What is the average traffic speed across all measurement points?
SELECT
    ROUND(AVG(speed)::numeric, 2) AS average_traffic_speed
FROM traffic_locations
WHERE speed > 0;

--6- What is the average traffic flow for positive and negative directions?
SELECT
    direction,
    ROUND(AVG(flow), 2) AS average_flow
FROM traffic_locations
GROUP BY direction;
--7- What is the average speed for positive and negative directions?
SELECT
    direction,
    ROUND(AVG(speed)::numeric, 2) AS average_speed
FROM traffic_locations
WHERE speed > 0
GROUP BY direction;

--8- Which roads have high traffic flow but low speed?
SELECT
    road_name,
    direction,
    "offset",
    flow,
    speed
FROM traffic_locations
WHERE flow > (
    SELECT AVG(flow)
    FROM traffic_locations
)
AND speed > 0
AND speed < (
    SELECT AVG(speed)
    FROM traffic_locations
    WHERE speed > 0
)
ORDER BY flow DESC;
--9- How many measurement points report zero traffic flow?
SELECT
    COUNT(*) AS zero_flow_points
FROM traffic_locations
WHERE flow = 0;

--10- Which roads have multiple traffic measurement points?

SELECT
    road_name,
    COUNT(*) AS measurement_points
FROM traffic_locations
GROUP BY road_name
HAVING COUNT(*) > 1
ORDER BY measurement_points DESC;